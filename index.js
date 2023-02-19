const { spawn } = require('child_process');

const python = spawn('python', ['main.py']);

python.stdout.on('data', (data) => {
  const json_data = JSON.parse(data.toString());
  console.log(json_data)
});

python.stderr.on('data', (data) => {
  console.error(data.toString());
});

python.on('close', (code) => {
  console.log(`child process exited with code ${code}`);
});
