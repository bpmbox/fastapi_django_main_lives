import data_loader
import data_processor
import model_trainer
import dashboard_generator

def main():
    # Load data
    data = data_loader.load_data()

    # Process data
    processed_data = data_processor.process_data(data)

    # Train model
    model = model_trainer.train_model(processed_data)

    # Generate dashboard
    dashboard_generator.generate_dashboard(model)

if __name__ == "__main__":
    main()