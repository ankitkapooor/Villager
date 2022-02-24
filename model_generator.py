from transformers import AutoModelForCausalLM, AutoTokenizer
import random

#tokenizer = AutoTokenizer.from_pretrained('Models/epochs_4/')
#model = AutoModelForCausalLM.from_pretrained('Models/epochs_4/')

tokenizer = AutoTokenizer.from_pretrained('Models/20K_steps/')
model = AutoModelForCausalLM.from_pretrained('Models/20K_steps/')

special_token = '<|endoftext|>'

class Generator:
    def __init__(self):
        self.tokenizer = tokenizer
        self.model = model

    def get_reply(user_input):
        prompt_text = f'User: {user_input}\nBot:'
        encoded_prompt = tokenizer.encode(prompt_text,
                                          add_special_tokens = False,
                                          return_tensors = 'pt')

        output_sequences = model.generate(
            input_ids = encoded_prompt,
            max_length = 200,
            temperature = 0.9,
            top_k = 20,
            top_p = 0.9,
            repetition_penalty = 1,
            do_sample = True,
            num_return_sequences = 4
        )

        result = tokenizer.decode(random.choice(output_sequences))
        result = result[result.index("Bot: "):result.index(special_token)]
        return(result[4:])
