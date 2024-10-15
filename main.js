const path = require("path");
const { app, BrowserWindow, Menu, ipcMain } = require("electron");
const { spawn } = require('child_process');
const axios = require('axios');
const fs = require('fs');

const isDev = process.env.NODE_ENV !== "development";
const isMac = process.platform === 'darwin';

function createMainWindow() {
    const mainWindow = new BrowserWindow({
        title: "Scheduler",
        width: isDev ? 1000 : 500,
        height: 600,
        frame : false,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false,
        }
    });

    if (isDev) {
        try {
            mainWindow.webContents.openDevTools();
        } catch (error) {
            console.error("Failed to open DevTools:", error);
        }
    }

    mainWindow.loadFile(path.join(__dirname, "./renderer/index.html"));
    mainWindow.setMenuBarVisibility(false); //Removes the menu bar ('file, edit, help')

    ipcMain.on('minimize-window', () => {
        mainWindow.minimize();
    });

    ipcMain.on('maximize-window', () => {
        if (mainWindow.isMaximized()) {
            mainWindow.unmaximize();
        } else {
            mainWindow.maximize();
        }
    });

    ipcMain.on('close-window', () => {
        mainWindow.close();
    });

    //Spawns the flask Server
    console.log("Spawning the Flask server...");
    const pythonProcess = spawn('python', [path.join(__dirname, 'backend/app.py')]);

    pythonProcess.stderr.on('data', (data) => {
        console.error(`Error from Python: ${data}`);
    });

    pythonProcess.on('close', (code) => {
        console.log(`Python process exited with code ${code}`);
    });
}

app.whenReady().then(() => {
    createMainWindow();

    const mainMenu = Menu.buildFromTemplate(menu);
    Menu.setApplicationMenu(mainMenu);

    app.on("activate", () => {
        if (BrowserWindow.getAllWindows().length === 0) {
            createMainWindow();
        }
    });
});

const menu = [
    {
        label: "File",
        submenu: [
            {
                label: "Quit",
                click: () => app.quit(),
                accelerator: "CmdOrCtrl+W"
            }
        ]
    }
];

app.on("window-all-closed", () => {
    axios.post('http://127.0.0.1:5000/close', { })
        .then(response => {
            if (!isMac) {
                app.quit();
            }
        })
        .catch(error => {
            if (!isMac) {
                app.quit();
            }
        });
});