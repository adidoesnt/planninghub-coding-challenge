import src.planninghub_coding_challenge.components.classifier as classifier
import src.planninghub_coding_challenge.components.utils.schema_generator as schema_generator
import src.planninghub_coding_challenge.constants as constants

if __name__ == "__main__":
    try:
        # TODO: Make schema generation part of the build process
        schema_generator = schema_generator.SchemaGenerator(config_path=constants.CONFIG_PATH, schema_path=constants.SCHEMA_PATH)
        schema = schema_generator.generate_schema()
        
        classifier = classifier.Classifier(config_path=constants.CONFIG_PATH)
    except Exception as e:
        print(f"[Main] Error: {e}")
        exit(1)
