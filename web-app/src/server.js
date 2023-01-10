const WebSocket = require("ws");
const Redis = require("ioredis");

const redisServerDetails = {
  host: "redis-17961.c135.eu-central-1-1.ec2.cloud.redislabs.com",
  port: 17961,
  password: "Cv8p67AgARkIjlchNpnCoAD7ZivsfsK3"
};

const sub = new Redis(redisServerDetails);
const pub = new Redis(redisServerDetails);
const WS_PORT = 3000;

sub.subscribe("ggadot", (err, count) => {
  if (err) {
    // Just like other commands, subscribe() can fail for some reasons,
    // ex network issues.
    console.error("Failed to subscribe: %s", err.message);
  } else {
    // `count` represents the number of channels this client are currently subscribed to.
    console.log(
      `Subscribed successfully! This client is currently subscribed to ${count} channels.`
    );
  }
});

const server = new WebSocket.Server({ port: WS_PORT });

server.on("connection", function connection(ws) {
  sub.on("message", (channel, message) => {
    console.log(`Received ${message} from ${channel}`);
    ws.send(message);
  });

  ws.on("message", message => {
    if (message == "server:connection:ping") {
      result = pub.ping();
      ws.send(`server:connection:${result}`);
    } else {
      pub.publish("ggadot", message);
    }
  });
});
