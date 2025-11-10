// server.js
const express = require("express");
const cors = require("cors");
const multer = require("multer");
const { v4: uuidv4 } = require("uuid");
const { spawn } = require("child_process");
const fs = require("fs");
const path = require("path");

const app = express();
app.use(cors());
app.use(express.json());

// Create folders if not exist
if (!fs.existsSync("uploads")) fs.mkdirSync("uploads");
if (!fs.existsSync("subtitles")) fs.mkdirSync("subtitles");

// Multer setup for file uploads
const upload = multer({ dest: "uploads/" });

// Store connected clients for Server-Sent Events
let clients = {};

// ✅ Real-time progress endpoint
app.get("/progress/:id", (req, res) => {
  res.setHeader("Content-Type", "text/event-stream");
  res.setHeader("Cache-Control", "no-cache");
  res.setHeader("Connection", "keep-alive");
  res.flushHeaders();

  clients[req.params.id] = res;

  req.on("close", () => delete clients[req.params.id]);
});

// ✅ Main upload endpoint
app.post("/upload", upload.single("video"), (req, res) => {
  const videoFile = req.file.path;
  const lang = req.body.lang || "en"; // selected language (si, ta, hi, en)
  const srtFile = `subtitles/${uuidv4()}.srt`;
  const clientId = req.query.clientId;

  const send = (msg, percent) => {
    if (clientId && clients[clientId]) {
      clients[clientId].write(`data: ${JSON.stringify({ message: msg, percent })}\n\n`);
    }
  };

  send(`✅ Step 1: File uploaded successfully — ${req.file.originalname}`, 10);
  send(`🌐 Selected source language: ${lang}`, 15);
  send(`🎧 Step 2: Starting transcription + translation...`, 25);

  // spawn Python process
  const python = spawn("python", ["generate_subtitles.py", videoFile, srtFile, lang]);

  python.stdout.on("data", (data) => {
    const msg = data.toString("utf-8").trim();
    console.log(msg);
    send(msg, 50);
  });

  python.stderr.on("data", (data) => {
    console.error(data.toString());
    send(`⚠️ Python error: ${data.toString()}`, 75);
  });

  python.on("close", () => {
    if (fs.existsSync(srtFile)) {
      send("✅ Step 5: Subtitle generation finished!", 90);

      // send SRT file to client
      res.download(srtFile, req.file.originalname.replace(/\.\w+$/, ".srt"), (err) => {
        if (err) console.error(err);

        // cleanup
        fs.unlink(videoFile, () => {});
        fs.unlink(srtFile, () => {});
        send("🧹 Step 6: Temporary files deleted", 100);

        if (clientId && clients[clientId]) {
          clients[clientId].write(`data: ${JSON.stringify({ done: true })}\n\n`);
          clients[clientId].end();
          delete clients[clientId];
        }
      });
    } else {
      res.status(500).send("Subtitle generation failed.");
      send("❌ Subtitle generation failed.", 100);
    }
  });
});

app.listen(4000, () => console.log("✅ Server running on http://localhost:4000"));
