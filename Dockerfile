##
## @see https://hub.docker.com/_/python#:~:text=How%20to%20use%20this%20image
##
FROM python:3.11-alpine
LABEL authors="zedling"

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# RUN python -m build --sdist source-tree-directory

CMD [ "python", "./main.py" ]