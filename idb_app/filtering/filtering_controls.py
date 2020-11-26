# technically represented with a html dropdown
class RadioButton:
    def __init__(self, html_id:str, name:str, value:str, label:str):
        self.html_id = html_id
        self.name = name
        self.value = value
        self.label = label


class RadioButtonSet:
    def __init__(self, title:str, set_name:str, values:list, labels:list):
        self.title = title
        self.buttons = [
            RadioButton(html_id=f"radio_btn_{set_name}_{v}",
                        name=set_name,
                        value=v,
                        label=labels[i])
            for i, v in enumerate(values)]


class TextInput:
    def __init__(self, html_id:str, name:str, placeholder:str):
        self.html_id = html_id
        self.name = name
        self.placeholder = placeholder
