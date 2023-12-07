const express=require("express")
const http=require("http")
const ejs=require("ejs")
const path=require("path")
const multer=require("multer")
const { exec } = require('child_process')

const port = process.env.PORT || 5000

const app=express()
app.use(express.json())
app.use(express.urlencoded({extended:false}))
app.use(express.static("public")) 

const templatepath=path.join(__dirname,'public')
app.set("view engine","ejs")
app.set("views",templatepath)

const storage = multer.diskStorage({
    destination: function (req, file, cb) {
      cb(null, 'uploads')
    },
    filename: function (req, file, cb) {
      cb(null, "input"+path.extname(file.originalname) )
    }
  })
  
const upload = multer({ storage: storage })
f=false
app.get("/",async (req,res)=>{
    res.render("index",{data:f})
})

app.post('/index', upload.single('input'), (req, res) => {
    if (req.file) {
        exec('python3 backend_ml.py', (error, stdout, stderr) => {
            if (error) {
                console.error(`Error executing backend_ml.py: ${error.message}`);
                res.status(500).send('Internal Server Error');
                return;
            }
            f=true
            res.redirect("/");
        });
    } else {
        res.status(400).send('No file uploaded.');
    }
});
  

app.post('/download',async (req,res)=>{
    res.download("./uploads/output.mp4")
  
})
app.post('/reload',async (req,res)=>{
    f=false
    res.redirect('/')
  
})

app.listen(port,hostname,()=>{
    console.log("Server is Running!")
    })
    