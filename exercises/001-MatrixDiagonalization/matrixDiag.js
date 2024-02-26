const { exec } = require('child_process');
const winston = require('winston');
const os = require('os');
const { match } = require('assert');

const logger = winston.createLogger({
  level: 'info', 
  format: winston.format.combine(
    winston.format.timestamp({format: 'YYYY-MM-DD HH:mm:ss'}),
    winston.format.simple()
  ),
  eol: os.EOL,
  transports: [
    new winston.transports.File({ filename: 'matrixDiag.log' })
  ]
});

async function executePythonScript(script, args) {
    args_as_string = args.reduce((acc, arg) => acc + " " + arg, " ");
    return new Promise((resolve, reject) => {
      exec('python3 ' + script + args_as_string, (error, stdout, stderr) => {
        if (error) {
          reject(`Erreur lors de l'exécution du script Python : ${error}`);
          return;
        }
        if (stderr) {
          reject(`Erreur de sortie standard : ${stderr}`);
          return;
        }
        // La sortie standard (stdout) contient la valeur renvoyée par le script Python
        const valeurPython = stdout.trim();
        resolve(valeurPython);
      });
    });
  }

async function start(){
    try {
      logger.info("BEGIN SESSION : start");
      var valeur = await executePythonScript("exercises/001-MatrixDiagonalization/matrixDiag.py", ["start"]);
      valeur = JSON.parse(JSON.parse(JSON.stringify(valeur)).replace(/'/ig,'"'));
      logger.info(`END SESSION : start = ${valeur} of type ${typeof(valeur)}\n`);
      return valeur;
    } catch (error) {
      logger.error(`ERROR SESSION : start = ${error}\n`);
      return error;
    }
}

async function step1(seed, is_diag){
    try {
      logger.info("BEGIN SESSION : step1");
      var args = ["step1", "--seed", seed.toString()];
      if (is_diag){
          args.push("--is_diag");
      }
      const valeur = await executePythonScript("matrixDiag.py", args);
      console.log(`La valeur récupérée du script Python est : ${valeur}`);
      logger.info("END SESSION : step1\n");
    } catch (error) {
      logger.error("ERROR SESSION : step1\n");
    }
}

async function step2(seed, eigen){
  try {
    logger.info("BEGIN SESSION : step2");
    var args = ["step2", "--seed", seed.toString(), "--eigen", "'"+JSON.stringify(eigen)+"'"];
    const valeur = await executePythonScript("matrixDiag.py", args);
    console.log(`La valeur récupérée du script Python est : ${valeur}`);
    logger.info("END SESSION : step2\n");
  } catch (error) {
    logger.error("ERROR SESSION : step2\n");
  }
}

async function matrixDiag(body){
  let step = body.step;
  switch (step){
    case 0:
      return await start();
    case 1:
      return await step1(props["seed"], props["is_diag"]);
    case 2:
      return await step2(props["seed"], props["eigen"]);
    default :
      throw new Error("Bad matrixDiag case : " + step);
  }
}

// (async () => await start())();

// (async () => await step1(1432, true))();

// (async () => await step2(1432, {"3":[5,7,1], "1":[5,7,1], "5":[5,7,1]}))();

module.exports = matrixDiag;