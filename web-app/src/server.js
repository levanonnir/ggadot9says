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
const outboundChannel = "ggadot";
const inboundChannel = "app";

sub.subscribe(inboundChannel, (err, count) => {
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
    // if (message == "server:connection:ping") {
    //   // async const result = pub.ping().then((err, res) => {
    //   //   result = res;
    //   // });
    //   // const response = `server:connection:${result}`;
    //   // ws.send(response);
    //   // console.log(`Sending to FE: ${response}`);
    // } else {
      console.log(`Publishing to server: ${message}`);
      pub.publish(outboundChannel, message);
    // }
  });
});
