const shmmap = require('shmmap');
var buf;
buf = shmmap.read_write("test_shared_memory", 2048);
console.log(buf)
