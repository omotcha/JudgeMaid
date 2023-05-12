## A prompt generator for fine-tuning

### Disclaimer:

- This is just a demo


### Basic steps:

1. prepare json files for data and place them in @tmp/target_json
2. generate prompts: call `save_jsonl()` @util/prompt/gen_prompt_ju_ft.py
3. use openai toolkit to prepare the final train/valid dataset

    ```openai tools fine_tunes.prepare_data -f <LOCAL_FILE>```

    LOCAL_FILE is the jsonl file saved @tmp/ju_prompts
4. fine-tune the model
5. retrieve the model if necessary. please refer to @analyze/retrieve_ft.py