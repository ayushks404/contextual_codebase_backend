import express from "express";
import { protect } from "../middleware/authmiddleware.js";
import { createproject  } from "../controllers/project_controllers.js";

const router = express.Router();

router.post("/" ,protect, createproject);
// router.get("/",protect,getproject);
export default router;