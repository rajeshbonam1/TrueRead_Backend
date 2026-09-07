FROM public.ecr.aws/lambda/python:3.11

# Copy and install dependencies
COPY lamdareq.txt ${LAMBDA_TASK_ROOT}/
RUN pip install --no-cache-dir -r ${LAMBDA_TASK_ROOT}/lamdareq.txt

# Copy all application code
COPY . ${LAMBDA_TASK_ROOT}/

# Verify handler exists (for debugging)
RUN ls -la ${LAMBDA_TASK_ROOT}/lambda_handler.py && \
    echo "=== lambda_handler.py content ===" && \
    cat ${LAMBDA_TASK_ROOT}/lambda_handler.py

# Set the handler
CMD ["lambda_handler.handler"]