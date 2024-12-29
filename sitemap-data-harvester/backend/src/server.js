const express = require('express');
const path = require('path');
const routes = require('./routes');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 5001;

app.use(express.json({ limit: '10kb' })); // Limiting JSON payload size to 10kb
app.use(express.urlencoded({ extended: true, limit: '10kb' })); // Limiting URL-encoded payload size

app.use(express.static(path.join(__dirname, '../public')));
app.use(cors());

app.use('/api', routes);


app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
