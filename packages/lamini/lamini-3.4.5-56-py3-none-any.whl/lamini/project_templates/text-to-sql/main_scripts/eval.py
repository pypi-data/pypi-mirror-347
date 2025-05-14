import argparse
from typing import Optional, Dict, Any
from lamini import Lamini
from lamini.experiment.metrics import Metrics

def write_results(results, output_dir):
    with open(output_dir, "w") as f:
        for result in results:
            f.write(f"{result}\n")

def run_inference(eval_data, model_name):
    generator = Lamini(model_name)
    results = generator.generate([data["input"] for data in eval_data])
    for instance, result in zip(eval_data, results):
        results.append({
            "input": instance["input"],
            "generated_output": result,
            "output": instance["output"],
        })
    return results

def evaluate(eval_data, metrics, output_dir, model_name: Optional[str], metrics_config: Optional[Dict[str, Any]]):
    if model_name:
        if "input" in eval_data[0]:
            raise ValueError("Eval data must contain 'input' key")
        eval_data = run_inference(eval_data, model_name)

    metrics_results = []
    for instance in eval_data:
        if "generated_output" not in instance or "output" not in instance:
            raise ValueError("Eval data must contain 'generated_output' and 'output' keys")
        generated_output = instance["generated_output"]
        expected_output = instance["output"]
        instance_metrics = {}
        
        for metric in metrics:
            if metric not in Metrics.metrics:
                raise ValueError(f"Metric {metric} not found")
                
            metric_func = Metrics.metrics[metric]
            metric_config = metrics_config.get(metric, {}) if metrics_config else {}
            
            # Get the base required arguments
            required_args = {
                'generated_output': generated_output,
                'expected_output': expected_output,
            }
            
            # Add any additional configuration parameters
            required_args.update(metric_config)
            
            try:
                instance_metrics[metric] = metric_func(**required_args)
            except TypeError as e:
                # If the function doesn't accept all arguments, try with just the base ones
                print(f"Warning: Metric '{metric}' doesn't accept all config parameters: {metric_config}. Falling back to base arguments only.")
                instance_metrics[metric] = metric_func(generated_output, expected_output)
        
        metrics_results.append(instance_metrics)
    
    write_results(metrics_results, output_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--eval-data", type=str, required=True)
    parser.add_argument("--model-name", type=str, required=False, default=None)
    parser.add_argument("--metrics", type=str, required=True)
    parser.add_argument("--output-dir", type=str, required=True)
    args = parser.parse_args()

    evaluate(args.eval_data, args.model_name, args.metrics, args.output_dir)
