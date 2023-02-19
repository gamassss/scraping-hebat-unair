const { spawn } = require("child_process");
const { Client, Events, GatewayIntentBits } = require("discord.js");
const { bot_token, channel_id } = require("./key.json");
const schedule = require("node-schedule");

const client = new Client({ intents: [GatewayIntentBits.Guilds] });

const runPythonScript = () => {
	// spawn main.py
  const python = spawn("python", ["main.py"]);
  python.stdout.on("data", (data) => {
		// fetch data
    const json_data = JSON.parse(data.toString());
    
		// build fields
    const { tugas } = json_data;
    const fields = [
      {
        name: "Tanggal",
        value: `${json_data.nama_hari}`,
        inline: false,
      },
    ];
    const obj_field = {};

    tugas.forEach((e) => {
      const obj_field = {};

      obj_field["name"] = e["nama_tugas"];
      obj_field["value"] = `Jam: ${e["deadline"]}`;
      obj_field["inline"] = false;

      fields.push(obj_field);
    });

    const channel = client.channels.cache.get(channel_id);

    // Embed messages
    const embedTugasMessage = {
      color: 0xffcd00,
      title: "Tugas Reminder",
      description: "Reminder Tugas Hari Terdekat",
      thumbnail: {
        url: "attachment://semangat.webp",
      },
      fields: fields,
      timestamp: new Date().toISOString(),
      footer: {
        text: "By using this service, you agreed to our Terms and Service",
      },
    };

    channel.send({
      embeds: [embedTugasMessage],
      files: [
        {
          attachment: "./semangat.webp",
          name: "semangat.webp",
        },
      ],
    });
  });

  python.stderr.on("data", (data) => {
    console.error(data.toString());
  });

  python.on("close", (code) => {
    console.log(`child process exited with code ${code}`);
  });
};

client.once(Events.ClientReady, (c) => {
  console.log(`Ready! Logged in as ${c.user.tag}`);

	// you can customize the time below so it run in specific time you want
	schedule.scheduleJob("0 18 * * *", runPythonScript);

  schedule.scheduleJob("0 21 * * *", runPythonScript);
});

client.login(bot_token);
