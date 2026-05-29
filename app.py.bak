import gradio as gr
from core.brain import VitalisBrain

# Instantiate the brain for the UI
brain = VitalisBrain()

def trigger_train():
    # Attempt to call the training method
    if hasattr(brain, 'train_mode'):
        return brain.train_mode()
    return "Error: train_mode method not defined in VitalisBrain."

def trigger_deploy():
    # Attempt to call the deployment method
    if hasattr(brain, 'deploy_mode'):
        return brain.deploy_mode()
    return "Error: deploy_mode method not defined in VitalisBrain."

with gr.Blocks() as demo:
    gr.Markdown("# Vitalis Core | Command Center")
    with gr.Row():
        btn_train = gr.Button("Train Engine")
        btn_deploy = gr.Button("Deploy")
    output = gr.Textbox(label="Status")
    
    btn_train.click(trigger_train, outputs=output)
    btn_deploy.click(trigger_deploy, outputs=output)

if __name__ == "__main__":
    demo.launch()
