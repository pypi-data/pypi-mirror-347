from tracker import Tracker

def main(save_path):

    
    try:
        t = Tracker(save_path)
        for epoch in range(5):
            metric_names = ["loss", "accuracy"]
            metric_values = [1.0 / (epoch + 1), 0.5 + 0.1 * epoch]
            t.log_metrics(epoch, metric_names, metric_values)
        t.save_metrics()
        loaded_metrics = t.load_metrics(save_path)
        imgs = t.graph_metrics(loaded_metrics, save_path="trackalpaca/")
        print("Saved", len(imgs), "images.")
    except Exception as e:
        print(f"error in __main__: {e}")


if __name__ == "__main__":
    save_path = "trackalpaca/example.json"
    main(save_path)