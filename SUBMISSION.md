# Heron File Classifier

A document classification system that uses multiple classification strategies to identify document types.

## Existing limitations

The existing filename based classifier simply checks the name of the file for the presence of 'invoice',
'bank_statement' or 'drivers license' in the filename, which would not match files unless they have those exact strings being present in the files. If files are named incorrectly, then this classification method will not work. If files are named incorrectly, the content of those files could offer some insight into what the files might be, and this is not being utilized.

## Approach

In order to improve the classification capabilities of this service, I implemented the following:

1. Extend support for a range of files:
  - In order to support a range of files such as PDFs, Word Documents, Excel Sheets, Text files and JPEGs, I implemented a range of text extractors, which will extract any text content present in these files for content based classification. 

2. Implement a few different classification strategies:
  - Filename classifier:
    - Extended the existing filename classifier with more filename patterns, to cover a wider
      variation of filenames
  - Fuzzy-matching classifier:
    - Created a fuzzylogic based classifier, which runs a fuzzy match based on pre-defined patterns
      on the filename
  - Regex-based classifier:
    - Runs a regex search on the file contents, based on a pre-defined set of regex patterns for
      different file types
  - TF-IDF classifier:
    - Uses a TF-IDF Naive Bayes classification model, which is trained on a small set of sample 
      data, for semantic closeness between the sample data and the file content.

3. Run the file classification in the following manner:

**Assumption**: This algorithm assumes that if a file is named correctly, the name actually corresponds to
the content in the file. For example, if a file is named invoice-123.pdf, the file is actually an invoice, and not a driver's license.
  - The first classifier that is run is the Filename-based Classifier. If this returns a classification
    match, we stop here and return the result. 
  - If Filename-based classifier fails, we run the Fuzzy logic classifier. If this returns a  classification match, we stop here and return the result.
  - If Fuzzy logic fails, we run the regex based classifier. If this returns a classification match, we stop here and return the result.
  - If Regex based classification fails, we run the TF-IDF based classifier. If this returns a classification match, we stop here and return the result.
  - If none of the above classifiers returns a match, we return an unknown file response

**Rationale**: Based on the assumption, we first run checks on the filename, since it would be much faster to run checks against the filename than the file content. If we cannot get a match based on filename, then we move over to analysing the content. Assuming most files are named correctly based on their contents, we should be able to quickly classify files based on filename only, and only have to refer to the content if the files are not named appropriately.


4. Convert the Flask application to a FastAPI one:

FastAPI is a framework that offers high-performance, async support, built-in validation, along with API documentation (If we choose to deploy this as a standalone service, and extend its capabilities.)

5. Make use of Docker

Inorder to make the classifier deployable, I created a Dockerfile and a docker compose yaml file, so that
this can be deployed as a standalone service if needed, thereby making it accessible to other users or services. The docker container can be deployed to AWS ECS or Kubernetes clusters, and can have auto-scaling setup to scale according to the traffic/load.

6. Added a Makefile for easier setup and testing

7. Added checks for filename and file size, along with extending the list of allowed extensions.


## Potential Improvements

1. We could extend the content based classification capabilities by making use of LLMs (hosted/paid models). We could extract the text content of files passed, and pass it to LLMs, which can classify it based on the file content.

2. Batch processing: We could allow for batches of files to be uploaded, for bulk classification. Depending on the performance capabilities, this may need to be exposed as an asynchronous funcitonality, ie, user uploads a batch of files and gets a job id in the response. Once the classifcation is complete, either user fetches the result, or a webhook notification can be sent.

3. Broader set of documents: Currently, we check for either invoice, bank statements or drivers license. This set can be widened to a larger set of document types, such as financial reports, inventory lists, etc.

4. Train custom models for classification: If we store the classification results for this service, this data could be used to train custom models, which could be plugged in at a later stage.

5. Setup CI/CD pipelines for automated deployments

6. Improve test coverage

7. Improved logging: Implementing a structured logging system, for improved debuggability. We can also push logs to Elasticsearch for improved analysis

8. Better edge case handling, handling corrupted files, checking files for vulnerabilities before processing.

9. Add Prometheus metrics, for better visibility into application metrics

10. Use poetry for dependency management, use uv for dependency installation.

11. Add pre-commit hooks and linters, for improved code structuring and to remove linter errors.

