import src.planninghub_coding_challenge.components.classifier as classifier

if __name__ == "__main__":
    try:
        classifier = classifier.Classifier(config_path="./config/planning-permission-rules-config.csv")
    except Exception as e:
        print(f"[Main] Error: {e}")
        exit(1)
