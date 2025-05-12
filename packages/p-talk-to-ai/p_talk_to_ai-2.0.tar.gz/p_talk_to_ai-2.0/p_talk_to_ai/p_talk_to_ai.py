import os
from openai import OpenAI
import pickle

class P_talk_to_ai:
    def __init__(self, name,api_key,base_url,model="deepseek-reasoner"):
        self.name = name
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.client = OpenAI(
            api_key = api_key,
            base_url = base_url,
        )
        if os.path.exists(f'{name}_tomb.pkl'):
            with open(f'{name}_tomb.pkl', 'rb') as f:
                self.messages = pickle.load(f)
        else:
            self.messages = []

    def save_to_hell(self):
        with open(f'{self.name}_tomb.pkl', 'wb') as f:
            pickle.dump(self.messages, f)

    def talk(self,content):
        #TODO 提问内容录入
        message={'role': 'user', 'content': content}
        #TODO 提问内容加入messages参数
        self.messages.append(message)
        #TODO 提问
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
        )
        #TODO 获取回复
        self.messages.append({'role': 'assistant', 'content': completion.choices[0].message.content})
        thinking = f'思考：\n{completion.choices[0].message.reasoning_content}'
        answer = f'回答：\n{completion.choices[0].message.content}'
        print(thinking)
        print(answer)
        return thinking,answer
    def new_talk(self):
        self.messages = []
    def stream_talk(self,content,thinking = True):
        reasoning_content = ""
        answer_content = ""
        is_answering = False
        message={'role': 'user', 'content': content}
        self.messages.append(message)
        stream = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            stream=True
            # 解除以下注释会在最后一个chunk返回Token使用量
            # stream_options={
            #     "include_usage": True
            # }
        )

        if thinking:
            print("\n" + "=" * 20 + "思考过程" + "=" * 20 + "\n")

        for chunk in stream:
            # 处理usage信息
            if not getattr(chunk, 'choices', None):
                print("\n" + "=" * 20 + "Token 使用情况" + "=" * 20 + "\n")
                print(chunk.usage)
                continue

            delta = chunk.choices[0].delta

            # 检查是否有reasoning_content属性
            if not hasattr(delta, 'reasoning_content'):
                continue

            # 处理空内容情况
            if not getattr(delta, 'reasoning_content', None) and not getattr(delta, 'content', None):
                continue

            # 处理开始回答的情况
            if not getattr(delta, 'reasoning_content', None) and not is_answering:
                print("\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n")
                is_answering = True

            # 处理思考过程
            if getattr(delta, 'reasoning_content', None) and thinking:
                print(delta.reasoning_content, end='', flush=True)
                reasoning_content += delta.reasoning_content
            # 处理回复内容
            elif getattr(delta, 'content', None):
                print(delta.content, end='', flush=True)
                answer_content += delta.content
        self.messages.append({'role': 'assistant', 'content': answer_content})
        self.save_to_hell()
    # 如果需要打印完整内容，解除以下的注释
    """
    print("=" * 20 + "完整思考过程" + "=" * 20 + "\n")
    print(reasoning_content)
    print("=" * 20 + "完整回复" + "=" * 20 + "\n")
    print(answer_content)
    """


if __name__ == '__main__':
    ai = aliAPI()
    ai.client()
    ai.stream_talk('python的魔术方法有哪些？')