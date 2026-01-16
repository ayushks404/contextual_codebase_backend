// import Project from "../models/project.js";
// import axios  from "axios";

// export const create_project = async (req , res) => {


//     try{

//         const {name , repourl } = req.body;

//         if (!repourl || !name ) {
//             return res.status(400).json({ message: "Please provide all fields" });
//         }

//         const urlExists = await user.findOne({ repourl });
//         if (urlExists) {
//             return res.status(400).json({ message: "project already exists" });
//         }


//         const project = await Project.create({
//             name,
//             repourl,
//             owner: req.user.id,
//             indexed: false
//         });
        
//         await axios.post("http://localhost:8000/index-repo", {
//             projectId: project._id,
//             repoUrl: project.repourl
//         });



//         res.status(201).json({
//             project
//         });

//     } catch (err){
//         res.status(500).json({
//             message: err.message
//         });
//     }


// };

import Project from "../models/project.js";
import axios from "axios";

export const createproject = async (req, res) => {
  try {

    const { name, repourl } = req.body;
    
    if (!name || !repourl) {
      return res.status(400).json({ message: "Name and repo URL required" });
    }

    // check duplicate
    const exists = await Project.findOne({ repourl });
    if (exists) {
      return res.status(400).json({ message: "Project already exists" });
    }

    const project = await Project.create({
      name,
      repourl,
      owner: req.user._id,
      indexed: false,
    });

    // call AI service to index repo (non-blocking)
    axios.post("http://localhost:8000/index-repo", {
      project_id: project._id,
      repo_url: repourl,
    }).catch(err => {
      console.log("AI indexing failed:", err.message);
    });



    res.status(201).json({ project });

  } catch (err) {
    console.error("Create project error:", err);
    res.status(500).json({ message: err.message });
  }
};


// export const getproject = async (req,res) =>{
//   try{
//     const project = await Project.findById(req.params.id)
//   }
// }