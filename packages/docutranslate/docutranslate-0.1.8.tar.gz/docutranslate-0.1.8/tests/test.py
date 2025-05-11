from docutranslate import FileTranslater
import time
start=time.time()
translater=FileTranslater(
    base_url=r"https://open.bigmodel.cn/api/paas/v4/",
    key="969ba51b61914cc2b710d1393dca1a3c.hSuATex5IoNVZNGu",
    model_id="glm-4-flash",
    max_concurrent=20
)

# translater=FileTranslater(
#     base_url=r"https://dashscope.aliyuncs.com/compatible-mode/v1",
#     key="sk-a3dd6bdedb5f446cbe678aedfab32038",
#     model_id="qwen-turbo",
#     chunksize=2000,
# )

translater.translate_file("./files/regex.md",
                          to_lang="中文",
                        #   refine=True,
                          formula=True,
                          code=True,
                          output_format="markdown")

print(f"耗时:{time.time()-start}")