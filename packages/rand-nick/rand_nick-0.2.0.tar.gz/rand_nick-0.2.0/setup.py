from setuptools import setup, find_packages

setup(
    name='rand_nick',  # Имя вашего пакета
    version='0.2.0',               # Версия вашего пакета
    packages=find_packages(),       # Автоматически находит все пакеты
    install_requires=[],            # Зависимости, если есть
    author='vsenikizanyati',             # Ваше имя
    author_email='fmsg4341@gmail.com',  # Ваш email
    description='Генератор никнеймов',  # Краткое описание
    long_description=open('README.md').read(),  # Длинное описание из README файла
    long_description_content_type='text/markdown',
    url='https://github.com/dsadasdasdsaas/rand_nick',  # URL вашего репозитория (если есть)
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.1',
)