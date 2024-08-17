import matplotlib.pyplot as plt

class ReportGenerator:
    def generate_text_report(product, sentiment_records):
        report_text = f"Sentiment Report for {product}:\n"
        for index, (sentiment_label, confidence_score) in enumerate(sentiment_records, start=1):
            confidence_score = float(confidence_score)
            report_text += f"Feedback {index}: Sentiment: {sentiment_label}, Confidence: {confidence_score:.2f}\n"
        return report_text


    def generate_graph(product, sentiment_records):
        sentiment_labels = [sentiment[0] for sentiment in sentiment_records]
        sentiment_counts = {label: sentiment_labels.count(label) for label in set(sentiment_labels)}
        plt.bar(sentiment_counts.keys(), sentiment_counts.values())
        plt.xlabel('Sentiment')
        plt.ylabel('Count')
        plt.title(f'Sentiment Distribution for {product}')
        plt.show()