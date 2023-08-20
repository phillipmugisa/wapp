import { WebSocketServer } from "ws";
import pkg from 'whatsapp-web.js';
const { Client, RemoteAuth, MessageMedia } = pkg;
import fs from 'fs'

const connectedUsers = new Map()
let myContacts = new Map()

// Require database
import { MongoStore } from 'wwebjs-mongo';
import mongoose from 'mongoose';

const MONGODB_URI = "mongodb://127.0.0.1:27017/wapp"

const server = new WebSocketServer({ port: 3000 });
server.on("connection", (socket) => {
    // send a message to the client
    console.log("New Connection Made")
    socket.on("message", (data) => {
        const packet = JSON.parse(data);
        switch (packet.type) {
            case "connect user":
                mongoose.connect(MONGODB_URI).then(() => {
                    const store = new MongoStore({ mongoose: mongoose });
                    const client = new Client({
                        authStrategy: new RemoteAuth({
                            clientId: packet.username,
                            store: store,
                            backupSyncIntervalMs: 300000
                        }),
                        puppeteer: {
                            args: ['--no-sandbox'],
                        }
                    });

                    client
                        .on('qr', (qr) => {
                            console.log("qr generated for ", packet.username)
                            socket.send(JSON.stringify({
                                type: "qr-code generated",
                                qrCode: qr
                            }));
                        });
                
                    client
                        .on('ready', async () => {
                            console.log("client ready for ", packet.username)
                            socket.send(JSON.stringify({
                                type: "account connected",
                            }));
                            connectedUsers.set(packet.username, client)
                        });

                    client
                        .on('authenticated', async (session) => {    
                            // Save the session object however you prefer.
                            // Convert it to json, save it to a file, store it in a database...
                            socket.send(JSON.stringify({
                                type: "authenticated",
                            }))
                            console.log("authenticated")
                        });
                    
                    
                    client
                        .on('remote_session_saved', () => {
                            console.log("remote_session_saved for ", packet.username)
                            socket.send(JSON.stringify({
                                type: "remote_session_saved",
                            }))
                        })
                    
                    client.initialize();
                });

                break;
                
            case "contacts":
                try {
                    let contacts_list = []
                    connectedUsers.get(packet.username)
                    .getContacts()
                    .then(contacts => {
                        if (!myContacts.get(packet.username)) {
                            myContacts.set(packet.username, contacts)
                        }
                        myContacts.get(packet.username)
                        .forEach(contact => {
                            if (contact.name != "...." && contact.id.server != "lid") {
                                let ct = {
                                    id: contact.id,
                                    name: contact.name,
                                    number: contact.id.user,
                                    isGroup: contact.isGroup,
                                    isBusiness: contact.isBusiness,
                                }
                                contacts_list.push(ct)
                            }
                        });
                        
                        socket.send(JSON.stringify({
                            type: "contact list",
                            contacts: contacts_list
                        }));
                    })
                }
                catch (err) {
                }
                break;
            case "send message":

                for (let item of packet.data.contacts) {
                    for (const file of packet.data.files) {
                        const fileData = file.fileData;
                        const fileName = file.fileName;

                        const data = fileData.replace(/^data:image\/\w+;base64,/, '');
                        const buffer = Buffer.from(data, 'base64');

                        fs.writeFileSync(fileName, buffer, {encoding: 'base64'});

                        const filePath = `./${fileName}`;
                  
                        const media = MessageMedia.fromFilePath(filePath);

                        if (packet.data.files.length == 1) {
                            connectedUsers.get(packet.username)
                            .sendMessage(item._serialized, media, { caption: packet.data.message })
                            .then(() => {
                                socket.send(JSON.stringify({
                                    type: "message sent",
                                }));
                            })
                            .catch ((err) => {
                                console.log(err)
                            })
                            .finally(() => {
                                fs.unlinkSync(filePath);
                            })
                        }
                        else {
                            connectedUsers.get(packet.username)
                            .sendMessage(item._serialized, media)
                            .then(() => {
                                socket.send(JSON.stringify({
                                    type: "message sent",
                                }));
                            })
                            .catch ((err) => {
                                console.log(err)
                            })
                            .finally(() => {
                                fs.unlinkSync(filePath);
                            })
                        }
                    }
                    if (packet.data.files.length != 1) {
                        console.log("message: ", item._serialized, packet.data.message)
                        connectedUsers.get(packet.username)
                        .sendMessage(item._serialized, packet.data.message)
                        .then(() => {
                            socket.send(JSON.stringify({
                                type: "message sent",
                            }));
                        })
                        
                    }
                }
                break;
        }
    });
    
    socket.on("close", (data) => {
        socket.close()
    })
});


const backendConnectionServer = new WebSocketServer({ port: 3030 });
backendConnectionServer.on("connection", (socket) => {
    // send a message to the client
    console.log("New Connection Made")
    socket.on("message", (data) => {
        const packet = JSON.parse(data);
        switch (packet.type) {
            case "connect user":
                mongoose.connect(MONGODB_URI).then(() => {
                    const store = new MongoStore({ mongoose: mongoose });
                    const client = new Client({
                        authStrategy: new RemoteAuth({
                            clientId: packet.username,
                            store: store,
                            backupSyncIntervalMs: 300000
                        }),
                        puppeteer: {
                            args: ['--no-sandbox'],
                        }
                    });
                    connectedUsers.set(packet.username, client)

                    connectedUsers.get(packet.username)
                        .on('qr', (qr) => {
                            console.log("qr generated for ", packet.username)
                            socket.send(JSON.stringify({
                                type: "qr-code generated",
                                qrCode: qr
                            }));
                        });
                
                    connectedUsers.get(packet.username)
                        .on('ready', async () => {
                            console.log("client ready for ", packet.username)
                            socket.send(JSON.stringify({
                                type: "account connected",
                            }));
                        });
                
                    connectedUsers.get(packet.username)
                        .on('message', async (message) => {
                            if (!message.isStatus) {
                                const contact = await message.getContact()
                                socket.send(JSON.stringify({
                                    type: "new-message",
                                    message: message,
                                    contact: contact.name
                                }));
                            }
                            else {
                                // statuses
                            }
                        });

                    connectedUsers.get(packet.username)
                        .on('authenticated', async (session) => {    
                            // Save the session object however you prefer.
                            // Convert it to json, save it to a file, store it in a database...
                            socket.send(JSON.stringify({
                                type: "authenticated",
                            }))
                        });
                    
                    connectedUsers.get(packet.username)
                        .initialize();
                });

                break;
                
            case "contacts":
                try {
                    let contacts_list = []
                    connectedUsers.get(packet.username)
                    .getContacts()
                    .then(contacts => {
                        if (!myContacts.get(packet.username)) {
                            myContacts.set(packet.username, contacts)
                        }
                        myContacts.get(packet.username)
                        .forEach(contact => {
                            if (contact.name != "...." && contact.id.server != "lid") {
                                let ct = {
                                    id: contact.id,
                                    name: contact.name,
                                    number: contact.id.user,
                                    isGroup: contact.isGroup,
                                    isBusiness: contact.isBusiness,
                                }
                                contacts_list.push(ct)
                            }
                        });
                        
                        socket.send(JSON.stringify({
                            type: "contact list",
                            contacts: contacts_list
                        }));
                    })
                }
                catch (err) {
                }
                break;
            case "send message":

                for (let item of packet.data.contacts) {
                    for (const file of packet.data.files) {
                        const fileData = file.fileData;
                        const fileName = file.fileName;

                        const data = fileData.replace(/^data:image\/\w+;base64,/, '');
                        const buffer = Buffer.from(data, 'base64');

                        fs.writeFileSync(fileName, buffer, {encoding: 'base64'});

                        const filePath = `./${fileName}`;
                  
                        const media = MessageMedia.fromFilePath(filePath);

                        if (packet.data.files.length == 1) {
                            connectedUsers.get(packet.username)
                            .sendMessage(item._serialized, media, { caption: packet.data.message })
                            .then(() => {
                                socket.send(JSON.stringify({
                                    type: "message sent",
                                }));
                            })
                            .catch ((err) => {
                                console.log(err)
                            })
                            .finally(() => {
                                fs.unlinkSync(filePath);
                            })
                        }
                        else {
                            connectedUsers.get(packet.username)
                            .sendMessage(item._serialized, media)
                            .then(() => {
                                socket.send(JSON.stringify({
                                    type: "message sent",
                                }));
                            })
                            .catch ((err) => {
                                console.log(err)
                            })
                            .finally(() => {
                                fs.unlinkSync(filePath);
                            })
                        }
                    }
                    if (packet.data.files.length != 1) {
                        console.log("message: ", item._serialized, packet.data.message)
                        connectedUsers.get(packet.username)
                        .sendMessage(item._serialized, packet.data.message)
                        .then(() => {
                            socket.send(JSON.stringify({
                                type: "message sent",
                            }));
                        })
                        
                    }
                }
                break;
        }
    });

});

// mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.10.3