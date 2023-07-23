import { WebSocketServer } from "ws";
import pkg from 'whatsapp-web.js';
const { Client, LocalAuth, MessageMedia } = pkg;
import fs from 'fs'

const server = new WebSocketServer({ port: 3000 });
let client;
let myContacts;


server.on("connection", (socket) => {
    // send a message to the client
    console.log("New Connection Made")
    socket.on("message", (data) => {
        const packet = JSON.parse(data);
        switch (packet.type) {
            case "connect user":
                client = new Client({
                    // authStrategy: new LocalAuth({ clientId: packet.username }),
                    puppeteer: {
                        args: ['--no-sandbox'],
                    }
                })
                client.on('qr', (qr) => {
                    socket.send(JSON.stringify({
                        type: "qr-code generated",
                        qrCode: qr
                    }));
                });
            
                client.on('ready', async () => {
                    socket.send(JSON.stringify({
                        type: "account connected",
                    }));
                });
            
                client.on('message', async (message) => {
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

                client.on('authenticated', async (session) => {    
                    // Save the session object however you prefer.
                    // Convert it to json, save it to a file, store it in a database...
                    socket.send(JSON.stringify({
                        type: "authenticated",
                    }))
                });                
                
                client.initialize();
                break;
            case "contacts":
                try {
                    let contacts_list = []
                    client.getContacts()
                    .then(contacts => {
                        myContacts = contacts
                        contacts.forEach(contact => {
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

                packet.data.contacts.forEach(async (item) => {
                    packet.data.files.forEach(async (fileData) => {
                        fs.writeFileSync(fileName, fileData, 'base64');

                        const filePath = `./${fileName}`;
                  
                        const media = MessageMedia.fromFilePath(filePath);

                        if (packet.data.files.length == 1) {
                            client.sendMessage(item._serialized, media, { caption: packet.data.message })
                            .then(() => {
                                socket.send(JSON.stringify({
                                    type: "message sent",
                                }));
                            })
                            .finally(() => {
                                fs.unlinkSync(filePath);
                            })
                        }
                        else {
                            client.sendMessage(item._serialized, media)
                            .then(() => {
                                socket.send(JSON.stringify({
                                    type: "message sent",
                                }));
                            })
                            .finally(() => {
                                fs.unlinkSync(filePath);
                            })
                        }
                    })
                    if (packet.data.files.length != 1) {
                        await client.sendMessage(item._serialized, packet.data.message);
                        
                        socket.send(JSON.stringify({
                            type: "message sent",
                        }));
                    }
                })
                break;
        }
    });

});