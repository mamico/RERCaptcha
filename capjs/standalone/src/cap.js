import Cap from "@cap.js/server";
import { Elysia } from "elysia";
import { cors } from "@elysiajs/cors";
import { db } from "./db.js";
import { rateLimit } from "elysia-rate-limit";
import { ratelimitGenerator } from "./ratelimit.js";

export const capServer = new Elysia({
	detail: {
		tags: ["Challenges"],
	},
})
	.use(
		rateLimit({
			scoping: "scoped",
			max: 45,
			duration: 5_000,
			generator: ratelimitGenerator,
		}),
	)
	.use(
		cors({
			origin: process.env.CORS_ORIGIN?.split(",") || true,
			methods: ["POST"],
		}),
	)
	.post("/:siteKey/challenge", async ({ set, params }) => {
		const cap = new Cap({
			noFSState: true,
		});
		const [_keyConfig] = await db`SELECT (config) FROM keys WHERE siteKey = ${params.siteKey}`;

		if (!_keyConfig) {
			set.status = 404;
			return { error: "Invalid site key or secret" };
		}

		const keyConfig = JSON.parse(_keyConfig.config);

		const challenge = await cap.createChallenge({
			challengeCount: keyConfig.challengeCount,
			challengeSize: keyConfig.saltSize,
			challengeDifficulty: keyConfig.difficulty,
			expiresMs: keyConfig.expiresMS || 600000,
		});

		await db`
			INSERT INTO challenges (siteKey, token, data, expires)
			VALUES (${params.siteKey}, ${challenge.token}, ${Object.values(challenge.challenge).join(",")}, ${challenge.expires})
		`;

		return challenge;
	})
	.post("/:siteKey/redeem", async ({ body, set, params }) => {
		const [_keyConfig] = await db`SELECT (config) FROM keys WHERE siteKey = ${params.siteKey}`;

		if (!_keyConfig) {
			set.status = 404;
			return { error: "Invalid site key or secret" };
		}

		const [challenge] = await db`
			SELECT * FROM challenges WHERE siteKey = ${params.siteKey} AND token = ${body.token}
		`;

		try {
			await db`DELETE FROM challenges WHERE siteKey = ${params.siteKey} AND token = ${body.token}`;
		} catch {
			set.status = 404;
			return { error: "Challenge not found" };
		}

		if (!challenge) {
			set.status = 404;
			return { error: "Challenge not found" };
		}

		const keyConfig = JSON.parse(_keyConfig.config);

		const cap = new Cap({
			noFSState: true,
			state: {
				challengesList: {
					[challenge.token]: {
						challenge: {
							c: challenge.data.split(",")[0],
							s: challenge.data.split(",")[1],
							d: challenge.data.split(",")[2],
						},
						expires: challenge.expires,
					},
				},
			},
		});

		const { success, token, expires } = await cap.redeemChallenge(body);
		// TODO: evaluate to have different token ttl than challenge ttl
		const expires_custom = Date.now() + (keyConfig.tokenTTL || 20 * 60 * 1000);

		if (!success) {
			set.status = 403;
			return { error: "Invalid solution" };
		}

		// console.log("Redeemed challenge, issuing token:", token, expires, expires_custom, expires === expires_custom);
		await db`
			INSERT INTO tokens (siteKey, token, expires)
			VALUES (${params.siteKey}, ${token}, ${expires_custom})
		`;

		const now = Math.floor(Date.now() / 1000);
		const hourlyBucket = Math.floor(now / 3600) * 3600;
		await db`
			INSERT INTO solutions (siteKey, bucket, count)
			VALUES (${params.siteKey}, ${hourlyBucket}, 1)
			ON CONFLICT (siteKey, bucket)
			DO UPDATE SET count = count + 1
		`;

		return {
			success: true,
			token,
			expires: expires_custom,
		};
	});
