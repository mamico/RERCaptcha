import { staticPlugin } from "@elysiajs/static";
import { swagger } from "@elysiajs/swagger";
import { Elysia, file } from "elysia";
import { assetsServer } from "./assets.js";
import { auth } from "./auth.js";
import { capServer } from "./cap.js";
import { server } from "./server.js";
import { siteverifyServer } from "./siteverify.js";

const serverPort = process.env.SERVER_PORT || 3000;
const serverHostname = process.env.SERVER_HOSTNAME || "0.0.0.0";
const iamServerName = process.env.IAM_SERVER_NAME;

new Elysia({
  serve: {
    port: serverPort,
    hostname: serverHostname,
  },
})
  .use(
    swagger({
      scalarConfig: {
        customCss: `.section-header-wrapper .section-header.tight { margin-top: 10px; }`,
      },
      exclude: ["/", "/auth/login"],
      documentation: {
        tags: [
          {
            name: "Keys",
            description:
              "Managing, creating and viewing keys. Requires API or session token",
          },
          {
            name: "Settings",
            description:
              "Managing sessions, API keys, and other settings. Requires API or session token",
          },
          {
            name: "Challenges",
            description: "Creating and managing challenges and tokens",
          },
          {
            name: "Assets",
            description: "Reading static assets from the assets server",
          },
        ],
        info: {
          title: "Cap Standalone",
          version: "2.0.0",
          description:
            "API endpoints for Cap Standalone. Both Keys and Settings endpoints require an API key or session token.\n\n[Learn more](https://capjs.js.org)",
        },
        securitySchemes: {
          apiKey: {
            type: "http",
          },
        },
      },
    })
  )
  .onBeforeHandle(({ set }) => {
    set.headers["X-Powered-By"] = "Cap Standalone";
  })
  .use(staticPlugin())
  .get("/", async ({ cookie, headers }) => {
    // DEBUG
    console.log("Headers in arrivo:", JSON.stringify(headers, null, 2));
    console.log("cap_authed:", cookie.cap_authed?.value);
    if (cookie.cap_authed?.value === "yes") {
      return file("./public/index.html");
    }
    else if (headers['x-forwarded-server'] === iamServerName) {
      console.log("autologin", headers['username']);
      return file("./public/autologin.html");
    }
    else {
      return file("./public/login.html");
    }
  })
  .use(auth)
  .use(server)
  .use(assetsServer)
  .use(capServer)
  .use(siteverifyServer)
  .listen(serverPort);

console.log(`🧢 Cap running on http://${serverHostname}:${serverPort}`);
