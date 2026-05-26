%%writefile engine_1.py
import torch
import numpy as np
import pymupdf4llm
from transformers import pipeline, AutoTokenizer, AutoModel, AutoModelForCausalLM, BitsAndBytesConfig

import hashlib
import os



class AdvancedResearchEngine:
    def __init__(
        self,
        model_name="mistralai/Mistral-7B-Instruct-v0.3",
        embed_model="allenai/scibert_scivocab_uncased"
    ):
        self.model_name  = model_name
        self.embed_model = embed_model
        self._cache      = {}

        # 1. HARDWARE DETECTION: Direct mapping to NVIDIA CUDA cores
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Executing Core Initializer on: {self.device.upper()}")

        # 2. TOKENIZER DESIGN: Prepares a strict text padding and attention matrix
        tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        tokenizer.model_max_length = 2048
        tokenizer.padding_side = "left" 

        if self.device == "cuda":
            # 3. 4-BIT QUANTIZATION LAYER: Compresses weights safely to avoid VRAM bloat
            quant_cfg = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="nf4",
            )
            
            model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                quantization_config=quant_cfg,
                device_map="auto" # Allocates network layers smoothly across active GPUs
            )
        else:
            model = AutoModelForCausalLM.from_pretrained(self.model_name, device_map="cpu")

        # Strip factory default length flags to avoid generation conflicts
        model.generation_config.max_length = None
        model.generation_config.max_new_tokens = 400

        # Construct the execution pipeline wrapper
        self.generator = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer
        )

        # 4. SCIBERT RETRIEVAL EMBEDDINGS: Accelerate vector searches on CUDA
        self.sci_tokenizer = AutoTokenizer.from_pretrained(self.embed_model)
        self.sci_model     = AutoModel.from_pretrained(self.embed_model)
        self.sci_model.eval()
        if self.device == "cuda":
def clear_engine_cache(self):
        self._cache.clear()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    def _scibert_encode(self, texts):
        if isinstance(texts, str):
            texts = [texts]
        encoded = self.sci_tokenizer(
            texts, padding=True, truncation=True,
            max_length=512, return_tensors="pt"
        )
        if self.device == "cuda":
            encoded = {k: v.to("cuda") for k, v in encoded.items()}
        with torch.no_grad():
            output = self.sci_model(**encoded)
        mask = encoded["attention_mask"].unsqueeze(-1).float()
        vecs = (output.last_hidden_state * mask).sum(1) / mask.sum(1)
        return vecs.cpu().numpy()

    def _retrieve_top_chunks(self, query, chunks, top_k=4):
        if not chunks:
            return []
        query_vec  = self._scibert_encode(query)[0]
        chunk_vecs = []
        for i in range(0, len(chunks), 16):
            chunk_vecs.append(self._scibert_encode(chunks[i:i+16]))
    chunk_vecs = np.vstack(chunk_vecs)
    sims = np.dot(chunk_vecs, query_vec) / (
            np.linalg.norm(chunk_vecs, axis=1) * np.linalg.norm(query_vec) + 1e-9
        )
    ranked = sorted(zip(sims, chunks), key=lambda x: x[0], reverse=True)
    return [c for _, c in ranked[:top_k]]

    def get_paper_sections(self, pdf_path):
        try: return pymupdf4llm.to_markdown(pdf_path)
        except: return ""

    def _file_hash(self, pdf_path):
        h = hashlib.md5()
        with open(pdf_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""): h.update(chunk)
        return h.hexdigest()

    def _split_chunks(self, raw_text):
        raw_chunks = [p.strip() for p in raw_text.split("\n\n") if len(p.strip()) >= 40]
        merged, buf = [], ""
        for c in raw_chunks:
            buf = (buf + "\n\n" + c).strip() if buf else c
            if len(buf) >= 350:  
                merged.append(buf)
                buf = ""
        if buf: merged.append(buf)
        return merged
def _generate(self, system_msg, user_msg):
        messages = [
            {"role": "system", "content": system_msg},
            {"role": "user",   "content": user_msg},
        ]
        out = self.generator(
            messages,
            max_new_tokens=400, 
            do_sample=True,
            temperature=0.1,
            repetition_penalty=1.2,
            truncation=True     
        )
        return out[0]["generated_text"][-1]["content"].strip()

    def analyze_and_run(self, pdf_path, progress_callback=None):
        file_hash = self._file_hash(pdf_path)
        if file_hash in self._cache:
            return self._cache[file_hash]

        raw_text = self.get_paper_sections(pdf_path)
        if not raw_text or len(raw_text.strip()) < 10:
            return {"error": "PDF text stream could not be loaded."}

        chunks = self._split_chunks(raw_text)
        arch_chunks = self._retrieve_top_chunks("model architecture layers channels dimensions convolutions parameters layers activation", chunks)
        metric_chunks = self._retrieve_top_chunks("results scores metrics accuracy fid evaluation findings table benchmarks values", chunks)
        impl_chunks = self._retrieve_top_chunks("implementation replication training hyperparameters learning rate optimizer setup steps", chunks)

        blueprint = self._generate(
            system_msg="You are a data extraction assistant. Extract ONLY the specific models, layers, and network details explicitly written in the text. If not in the text, say 'Not found'. Do not list generic libraries.",
            user_msg=f"List the model architecture details present in this text:\n\n{' '.join(arch_chunks)}"
        )

        metrics = self._generate(
            system_msg="You are a data validation tool. Extract only explicit named benchmarks accompanied by their numeric values. If no numbers are explicitly present, state 'No numbers reported.'",
            user_msg=f"List all numeric scores and statistical metrics found in this text:\n\n{' '.join(metric_chunks)}"
        )

        steps = self._generate(
            system_msg="You are an automation engineer. Write a concise, numbered list of implementation instructions based strictly on the parameters found in the text.",
            user_msg=f"Generate the execution steps from this text:\n\n{' '.join(impl_chunks)}"
        )

        result = {"blueprint": blueprint, "metrics": metrics, "steps": steps}
        self._cache[file_hash] = result
        return result
        
            
        
