# WhatsApp-Llama: Fine-tune Llama 7b to Mimic Your WhatsApp Style

samer

This repository is a fork of the `facebookresearch/llama-recipes`, adapted to fine-tune a Llama-2 7b chat model to replicate your personal WhatsApp texting style. By simply inputting your WhatsApp conversations, you can train the LLM to respond just like you do! Llama-2 7B chat is finetuned using parameter efficient finetuning (QLoRA) and int4 quantization on a single GPU (P100 with 16GB gpu memory).

## My Results

1. **Quick Learning**: The fine-tuned Llama-2 model picked up on my texting nuances rapidly.
   - The average words generated in the finetuned Llama-2 is *300%* more than vanilla Llama-2. I usually type longer replies, so this checks out
   - The model accurately replicated common phrases I say and my emoji usage
  
2. **Turing Test with Friends**: As an experiment, I asked my friends to ask me 3 questions on WhatsApp, and responded with 2 candidate responses (one from me and one from the LLM). My friends then had to guess which candidate response was mine and which one was Llama's.

The result? The model fooled *10%* (2/20) of my friends. Some of the model's responses were eerily similar to my own. Here are some examples (Candidate A is Llama-2 7B):

- *Example 1*: 
    <p align="center">
        <img width="628" alt="image" src="https://github.com/Ads-cmu/WhatsApp-Llama/assets/107292631/65361711-79eb-4cf1-862d-fae93a6b674a.png">
    </p>

- *Example 2*: 
    <p align="center">
        <img width="630" alt="image" src="https://github.com/Ads-cmu/WhatsApp-Llama/assets/107292631/700fadd0-086f-40fc-8337-5071accec94f.png">
    </p>
  
   I believe that with access to more compute, this number could easily be pushed to ~40% (which would be near random guessing).  

## Getting Started

Here's a step-by-step guide on setting up this repository and creating your own customized dataset:

### 1. Exporting WhatsApp Chats
Details on how to export your WhatsApp chats can be found [here](https://faq.whatsapp.com/1180414079177245/?cms_platform=android). I exported 10 WhatsApp chats from friends who I speak to often. Be sure to exclude media while exporting. Each chat was saved as `<friend_name>Chat.txt`.

### 2. Preprocessing the Dataset
Complete the steps below to convert the exported chat into a format suitable for training:

#### Convert text files to json:
```bash
python preprocessing.py <your_name> <your_contact_name> <friend_name> <friend_contact_name> <folder_path>
```
1. `your_name` refers to your name (Llama will learn this name)
2. `your_contact_name` refers to how you've saved your number on your phone
3. `friend_name` refers to the name of your friend (Llama will learn this name)
4. `friend_contact_name` refers to the name you've used to save your friend's contact
5. `folder_path` should be the path in which you've stored your whatsapp chats.

You'll need to run this command once for every friend's chat you've exported
#### Convert json files to csv
Once you're done converting all texts to json, you can run the command below to create the dataset 
```bash
python prepare_dataset.py <dataset_folder> <your_name> <save_file>
```
1. `dataset_folder` refers to the folder with your json files
2. `your_name` refers to your name (Llama will learn this name)
3. `save_file` file path of the final csv

### 3. Validating the Dataset
Here's the expected format for the preprocessed dataset:

```
| ID |   Context  |    Reply   |
| -- | ---------- | ---------- |
| 1  | You: Hi    | What's up? |
|    | Friend: Hi |            |

```

Ensure your dataset looks like the above to verify you've done it correctly.

### 4. Model Configuration
Once you're done with the above steps, run WhatsApp_Finetune.ipyb

- If you're using a **P100 GPU**, load the model in **4 bits**:

- If you're using an **A100 GPU**, you can load the model in **8 bits**:

PEFT adds around 4.6M parameters, or 6% of total model weights.

Additionally, you'll need to make the following 2 changes to `ft_datasets/whatsapp_dataset.py`:
1. Update the prompt to one of your choosing (line 8)
2. Update the file path of your dataset in the dataset.load_dataset() command (line 5)

### 5. Training Time
For reference, a 10MB dataset will complete 1 epoch in approximately 7 hours on a P100 GPU. My results shared above were achieved after training for just 1 epoch.

## Conclusion

This adaptation of the Llama model offers a fun way to see how well a LLM can mimic your personal texting style. Remember to use AI responsibly and inform your friends if you're using the model to chat with them!

---



