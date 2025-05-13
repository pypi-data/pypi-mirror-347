from setuptools import setup, find_packages  # type: ignore

DESCRIPTION = "LLM Agent Toolkit provides minimal, modular interfaces for core components in LLM-based applications."

# python3 setup.py sdist bdist_wheel
# twine upload --skip-existing dist/* --verbose

VERSION = "0.0.33.1"

with open("./README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

core_dependencies = [
    "python-dotenv==0.21.0",
    "charade==1.0.3",
    "openai==1.66.5",
    "tiktoken==0.9.0",
    "chromadb==0.5.11",
    "faiss-cpu==1.9.0.post1",
    "aiohttp==3.10.11",
    "pdfplumber==0.11.4",
    "PyMuPDF==1.24.11",
    "python-docx==1.1.2",
]
transformers_dependencies = [
    "torch==2.6.0",
    "transformers==4.50.0",
]
transcriber_dependencies = [
    "pydub==0.25.1",
    "pydub-stubs==0.25.1.4",
    "ffmpeg-python==0.2.0",
    "setuptools-rust==1.10.2",
    "openai-whisper==20240930",
]
gemini_dependencies = ["google-genai==1.0.0"]
ollama_dependencies = ["ollama==0.4.4"]

extras = {
    "transformers": transformers_dependencies,
    "transcriber": transcriber_dependencies,
    "gemini": gemini_dependencies,
    "ollama": ollama_dependencies,
    "all": [
        *transformers_dependencies,
        *transcriber_dependencies,
        *gemini_dependencies,
        *ollama_dependencies,
    ],
}

setup(
    name="llm_agent_toolkit",
    version=VERSION,
    packages=find_packages(),
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="jonah_whaler_2348",
    author_email="jk_saga@proton.me",
    license="GPLv3",
    install_requires=core_dependencies,
    extras_require=extras,
    keywords=[
        "llm",
        "agent",
        "toolkit",
        "large language model",
        "memory management",
        "tool integration",
        "multi-modality interaction",
        "multi-step workflow",
        "vision",
        "tools",
        "structured output",
        "chunking",
        "chromadb",
        "faiss",
        "ollama",
        "openai",
        "deepseek",
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.10",
    ],
)
