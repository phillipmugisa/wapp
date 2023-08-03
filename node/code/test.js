import { MongoStore } from 'wwebjs-mongo';
import mongoose from 'mongoose';
import pkg from 'whatsapp-web.js';
const { Client, RemoteAuth } = pkg;

const MONGODB_URI = "mongodb://127.0.0.1:27017/wapp"

mongoose.connect(MONGODB_URI)
    .then(() => {
        console.log("connected")
        const store = new MongoStore({ mongoose: mongoose });
        const client = new Client({
            restartOnAuthFail: true,
            authStrategy: new RemoteAuth({
                store: store,
                backupSyncIntervalMs: 300000
            }),
            puppeteer: {
                args: ['--no-sandbox'],
            }
        });

        client.on('remote_session_saved', () => {
            console.log("remote_session_saved")
        })

        
        client
        .on('qr', (qr) => {
            console.log("qr generated for ", packet.username)
            console.log(qr)
        });

        client.initialize();
    })
