import uvicorn
from docutranslate.app import app
uvicorn.run(app, host="127.0.0.1", port=8010)

import docling.models.factories.base_factory
easyocr