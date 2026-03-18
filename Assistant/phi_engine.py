import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

BASE_MODEL = "microsoft/phi-1_5"
LORA_PATH = "/Users/prashanth/Documents/Yukino_AI/Assistant/yukino_phi2_lora_model (1)"

# 🔥 Use Apple GPU
device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")

tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)

base_model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL,
    torch_dtype=torch.float32  # 🔥 half precision
)

model = PeftModel.from_pretrained(base_model, LORA_PATH)

# 🔥 Merge LoRA for speed
model = model.merge_and_unload()

model.to(device)
model.eval()


def inject_yukino_personality(reasoned_text: str) -> str:

    template = (
        "Yukinoshita Yukino rewrites the following response.\n"
        "She is calm, sharp, and intellectually dominant.\n"
        "She exposes flawed reasoning without being emotional.\n"
        "She avoids clichés and motivational language.\n"
        "Maximum 2 sentences.\n\n"
        f"Text:\n{reasoned_text}\n\nYukino:"
    )

    inputs = tokenizer(template, return_tensors="pt").to(device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=35,
            do_sample=False,
            repetition_penalty=1.1,
            no_repeat_ngram_size=3,
            eos_token_id=tokenizer.eos_token_id,
            pad_token_id=tokenizer.eos_token_id
        )

    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
    reply = decoded.split("Yukino:")[-1]
    return reply.strip()

