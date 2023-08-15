import gradio as gr
from pathlib import Path
from modules import script_callbacks, shared
# Webui root path
ROOT_DIR = Path().absolute()
import json
import os
import functools
from modules import paths
# 获取当前文件的根目录
root_directory = os.path.dirname(os.path.abspath(__file__))

# 获取根目录的父目录
parent_directory = os.path.dirname(root_directory)

# 调用函数并传入文件夹路径和config.json文件路径
folder_path = parent_directory+"\models"
config_file = parent_directory+"\config.json"
file_config = parent_directory+"\fileConfig.json"
# 创建多个CheckBox
checkboxes = []
textboxs = []
def update_config(folder_path, config_file):
    # 遍历文件夹
    for root, dirs, files in os.walk(folder_path):
        for dir_name in dirs:
            # dir_path = os.path.join(root, dir_name)
            has_required_files = ""
            
            # # 检查文件夹中是否有指定后缀的文件
            # for file_name in os.listdir(dir_path):
            #     if file_name.endswith(json.loads(file_config)["fileConfig"]):
            #         has_required_files = ""
            #         break
            
            # 更新config.json文件
            config_data = {}
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    config_data = json.load(f)
            
            config_data[dir_name] = str(has_required_files)
            
            with open(config_file, 'w') as f:
                json.dump(config_data, f, indent=4)
            
            print(f"文件夹 {dir_name} 更新成功")


# 获取json里面数据
def get_json_data(src):
    with open(src, 'rb') as f:  # 使用只读模型，并定义名称为f
        params = json.load(f)  # 加载json文件
        # params["code"] = "404"  # code字段对应的值修改为404
        # print("params", params)  # 打印
    return params  # 返回修改后的内容
 
 
# 写入json文件
def write_json_data(params):
    # 使用写模式，名称定义为r
    #其中路径如果和读json方法中的名称不一致，会重新创建一个名称为该方法中写的文件名
    with open('D:\z\mytest\htest.json', 'w') as r:
        # 将dict写入名称为r的文件中
        json.dump(params, r)



# 定义回调函数，用于获取CheckBox的选中状态
def get_checkbox_values(*checkboxes):
    values = {}
    for checkbox in checkboxes:
        checkbox_id = checkbox.elem_id
        value = gr.Interface(inputs=checkboxes).get_instances
        values[checkbox_id] = value
    return values

def create_symbolic_links(source_folder, target_folder):
    # 获取源文件夹中的所有文件
    files = os.listdir(source_folder)
    
    # 遍历每个文件，并创建符号链接到目标文件夹
    for file in files:
        source_path = os.path.join(source_folder, file)
        target_path = os.path.join(target_folder, file)
        # 检查目标路径是否已经存在
        if os.path.lexists(target_path):
            print("目标路径已存在，跳过创建符号链接")
        else:
        # 创建符号链接
            os.symlink(source_path, target_path)
            print(f"Created symbolic link for {file}")

def create_symbol_link():
    selectKey = []
    selectPath = []
    for checkbox, textbox in zip(checkboxes, textboxs):
            print(textbox.value)
            print(checkbox.value)
            if checkbox.value:
                selectKey.append(textbox.label)
                selectPath.append(textbox.value)
    print(checkboxes)
    print(textboxs)
    print(selectKey)
    print([checkbox.value for checkbox in checkboxes])
    for i in range(len(selectKey)):
        print(f"------{selectKey[i]}:{selectPath[i]}")
        create_symbolic_links(selectPath[i],os.path.join(paths.models_path, selectKey[i]))
        # j.elem_id == i.elem_id and get_checkbox_values(checkboxes=checkboxes) 

def checkbox_callback(checkbox_value):
    if checkbox_value:
        print("Checkbox is checked")
    else:
        print("Checkbox is unchecked")
        
def on_checkbox_change(key,checkbox):
    if key is not None:
        for cb in checkboxes:
            if cb.elem_id == key:
                cb.value = checkbox
                print(cb.elem_id,checkbox,"find")
                break

def on_textbox_change(key,checkbox):
    if key is not None:
        for cb in textboxs:
            if cb.elem_id == key:
                cb.value = checkbox
                print(cb.elem_id,checkbox,"find")
                break
      
def on_ui_tabs():
    file_json = get_json_data(config_file)
    with gr.Blocks(analytics_enabled=False) as ModelsPath_Blocks:
        gr.HTML(
            "<p id='change',style=\"margin-bottom:0.75em\">input custom path for models</p>")
        with gr.Column():
            for key, value in file_json.items():
                print(key,value)
                with gr.Row(scale=45):
                    textbox_info = gr.Textbox(label=key, value=value,
                                            readonly=False, elem_id=key)
                    textbox_info.change(functools.partial(on_textbox_change, textbox_info.elem_id), textbox_info)
                    textboxs.append(textbox_info)
                    checkBox = gr.Checkbox(value=value!='', elem_id=key,label='enable')
                    checkBox.change(functools.partial(on_checkbox_change, checkBox.elem_id), checkBox)
                    checkboxes.append(checkBox)
            with gr.Column(scale=80):
                change_btn = gr.Button(value="change", variant='primary', elem_id="change_btn")
                change_btn.click(fn=create_symbol_link)
    return [(ModelsPath_Blocks, "Models Manager", "Models Manager")]
script_callbacks.on_ui_tabs(on_ui_tabs)