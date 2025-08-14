import spacy
from spacy.tokens import Doc, DocBin
from spacy.util import filter_spans
from spacy.cli.train import train
from training_data import TRAIN_DATA
from datetime import datetime

def validate_data(data):
    """Checks for overlapping entities in the training data."""
    nlp = spacy.blank("en")
    print("--- 🧐 Verifying Training Data ---")
    for text, annotations in data:
        doc = nlp.make_doc(text)
        ents = []
        for start, end, label in annotations.get("entities"):
            span = doc.char_span(start, end, label=label)
            if span is None:
                print(f"\n--- 💥 ERROR: Misaligned Entity 💥 ---")
                print(f"Text: '{text}'")
                print(f"Annotation: ({start}, {end}, '{label}')")
                return False
            ents.append(span)
        
        filtered_ents = filter_spans(ents)
        if len(filtered_ents) < len(ents):
            print(f"\n--- 💥 ERROR: Overlapping Entity 💥 ---")
            print(f"Text: '{text}'")
            print(f"Annotations: {annotations.get('entities')}")
            return False
            
    print("--- ✅ Verification Complete: No errors found ---")
    return True

def create_docbin(data):
    """Creates a DocBin object from the training data."""
    nlp = spacy.blank("en")
    db = DocBin()
    for text, annotations in data:
        doc = Doc(nlp.vocab, words=text.split())
        ents = []
        for start, end, label in annotations.get("entities"):
            span = doc.char_span(start, end, label=label, alignment_mode="expand")
            if span is not None:
                ents.append(span)
        doc.ents = ents
        db.add(doc)
    return db

def run_training():
    if not validate_data(TRAIN_DATA):
        return

    db = create_docbin(TRAIN_DATA)
    db.to_disk("./training_data.spacy")

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_path = f"./output_model_{timestamp}"
    print(f"\n--- Saving new model to: {output_path} ---")

    print("\n--- 🚀 Starting Training ---")
    train(
        "./config.cfg",
        output_path,
        overrides={
            "paths.train": "./training_data.spacy",
            "paths.dev": "./training_data.spacy",
        },
    )
    print("--- 🎉 Training Complete ---")

if __name__ == "__main__":
    run_training()