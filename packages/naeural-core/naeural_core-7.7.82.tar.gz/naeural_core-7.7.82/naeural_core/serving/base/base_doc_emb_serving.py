from naeural_core.serving.base.base_llm_serving import BaseLlmServing as BaseServingProcess
from transformers import AutoTokenizer, AutoModel
import re

from docarray import BaseDoc, DocList
from docarray.typing import NdArray
from vectordb import HNSWVectorDB


"""
  TODO:
  - integrate vectordb library
  - add segmentation of the context
  - support multiple sets of context(maybe a dictionary of format {key: list[doc1, doc2, ...]})
  - add context to a single set
  - change context for a single set
  - reset all sets of context
  
"""


__VER__ = '0.1.0.0'
EMBEDDING_SIZE = 512
MAX_SEGMENT_SIZE = 300
MAX_SEGMENT_OVERLAP = 30
WORD_FIND_REGEX = r'\b(?:[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}|[a-zA-Z]+(?:\'[a-z]+)?|[0-9]+(?:\.[0-9]+)?|[^\s\w])\b'
DEFAULT_NUMBER_OF_RESULTS = 10

_CONFIG = {
  **BaseServingProcess.CONFIG,

  'MAX_BATCH_SIZE': 32,
  'MAX_EMB_SIZE': EMBEDDING_SIZE,
  'RUNS_ON_EMPTY_INPUT': True,

  'VALIDATION_RULES': {
    **BaseServingProcess.CONFIG['VALIDATION_RULES'],
  },

}


class DocEmbCt:
  REQUEST_TYPE = 'REQUEST_TYPE'
  REQUEST_ID = 'REQUEST_ID'
  REQUEST_PARAMS = 'REQUEST_PARAMS'

  QUERY = 'QUERY'
  ADD_DOC = 'ADD_DOC'
  LIST_CONTEXT = 'LIST_CONTEXT'

  BAD_REQUEST = 'BAD_REQUEST'
  ERROR_MESSAGE = 'ERROR_MESSAGE'
  DEFAULT_REQUEST_TYPE = QUERY
  REQUEST_TYPES = [QUERY, ADD_DOC, LIST_CONTEXT]

  DOC_KEY = 'doc'
  DOCS_KEY = 'docs'
  URL_KEY = 'url'
  AVAILABLE_DOCS = ['doc', 'docs']
# endclass


class NaeuralDoc(BaseDoc):
  # TODO: encrypt the text for db and decrypt it when needed.
  text: str = ''
  embedding: NdArray[EMBEDDING_SIZE]
  idx: int = -1
# endclass


class DocSplitter:
  """
  Class for splitting one document or a list of documents into segments.
  """
  def __init__(
      self, max_segment_size: int = MAX_SEGMENT_SIZE,
      max_segment_overlap: int = MAX_SEGMENT_OVERLAP,
  ):
    """
    Constructor for the DocSplitter class.

    Parameters
    ----------
    max_segment_size : int - the maximum size of a segment in words
    max_segment_overlap : int - the maximum overlap between segments in words
    """
    self.__max_segment_size = max_segment_size
    self.__max_segment_overlap = max_segment_overlap
    return

  def document_atomizing(self, document: str):
    """
    Atomize a document into words.

    Parameters
    ----------
    document : str - the document to be atomized

    Returns
    -------
    list[str] - the list of words
    """
    return re.findall(WORD_FIND_REGEX, document)

  def compute_best_overlap(self, text_size: int):
    """
    Compute the best overlap for the segments, while considering the text size and the maximum segment size.

    Parameters
    ----------
    text_size : int - the size of the text

    Returns
    -------
    int - the best overlap for the segments
    """
    # In case the text size is smaller than the maximum segment size, we do not need any overlap.
    if text_size <= self.__max_segment_size:
      return 0
    # We want the last segment to be as long as possible.
    best_overlap, best_last_segment_length = 0, 0
    # We cannot have an overlap larger than the maximum segment overlap.
    max_overlap = min(self.__max_segment_overlap, self.__max_segment_size - 1)
    min_overlap = int(max_overlap // 2)
    # The overlap between the segments helps us keep as much information as possible.
    # Thus, we start from half of the maximum overlap and go up to the maximum overlap.
    for overlap in range(min_overlap, max_overlap + 1):
      last_segment_length = (text_size - self.__max_segment_size) % (self.__max_segment_size - overlap)
      if last_segment_length > best_last_segment_length:
        best_overlap, best_last_segment_length = overlap, last_segment_length
      # endif last segment length is better
    # endfor each overlap
    return best_overlap

  def split_document(self, document: str):
    """
    Split a document into segments.

    Parameters
    ----------
    document : str - the document to be split

    Returns
    -------
    list[str] - the list of segments
    """
    # Break the document in words.
    words = self.document_atomizing(document)
    # Compute the best overlap for the segments.
    overlap = self.compute_best_overlap(text_size=len(words))
    increment_step = max(1, self.__max_segment_size - overlap)
    # Split the document into segments.
    segments = [
      ' '.join(words[i:i + self.__max_segment_size])
      for i in range(0, max(1, len(words) - overlap), increment_step)
    ]
    return segments

  def split_documents(self, documents: list[str]):
    """
    Split a list of documents into segments.
    Each document will be split into segments on its own, but the segmentations will be concatenated.

    Parameters
    ----------
    documents : list[str] - the list of documents to be split

    Returns
    -------
    list[str] - the list of segments
    """
    segmentations = [self.split_document(doc) for doc in documents]
    return sum(segmentations, [])
# endclass DocSplitter


class BaseDocEmbServing(BaseServingProcess):
  CONFIG = _CONFIG
  def __init__(self, **kwargs):
    super(BaseDocEmbServing, self).__init__(**kwargs)
    self.__dbs = {}
    self.__doc_splitter = DocSplitter()
    return

  def __context_identifier(self, context):
    return 'default' if context is None else f'context_{context}'

  def __db_cache_workspace(self, context):
    return self.os_path.join(self.get_models_folder(), 'vectordb', self.cfg_model_name, context)

  def __backup_contexts(self):
    """
    Backup the contexts to ensure their persistence.
    """
    self.persistence_serialization_save(
      obj={
        'contexts': list(self.__dbs.keys())
      }
    )
    return

  def __maybe_load_backup(self):
    """
    In case of persisted contexts, load them.
    """
    saved_data = self.persistence_serialization_load()
    if saved_data is not None:
      contexts = saved_data.get('contexts', [])
      for context in contexts:
        if context not in self.__dbs:
          self.__dbs[context] = HNSWVectorDB[NaeuralDoc](workspace=self.__db_cache_workspace(context))
        # endif sanity check in case of db already loaded
      # endfor each context
    # endif saved data available
    return

  def on_init(self):
    super(BaseDocEmbServing, self).on_init()
    self.__maybe_load_backup()
    return

  def _setup_llm(self):
    # just override this method as the base class has a virtual method that raises an exception
    return

  def _get_device_map(self):
    return self.device

  def load_tokenizer(self, model_id, cache_dir, token):
    self.tokenizer = AutoTokenizer.from_pretrained(
      model_id,
      cache_dir=self.cache_dir,
      use_auth_token=self.hf_token
    )
    return

  def load_pretrained_model(self, model_id, **kwargs):
    return AutoModel.from_pretrained(model_id, **kwargs)

  def _warmup(self):
    warmup_context = [
      "The Tesla Cybertruck is a battery electric pickup truck built by Tesla, Inc. since 2023.[6] Introduced as a "
      "concept vehicle in November 2019, it has a body design reminiscent of low-polygon modelling, consisting of flat "
      "stainless steel sheet panels.\nTesla initially planned to produce the vehicle in 2021, but it entered "
      "production in 2023 and was first delivered to customers in November. Three models are offered: a tri-motor "
      "all-wheel drive (AWD) \"Cyberbeast\", a dual-motor AWD model, and a rear-wheel drive (RWD) model, with EPA "
      "range estimates of 250–340 miles (400–550 km), varying by model.\nAs of December 2023, the Cybertruck is "
      "available only in North America.",

      "Am facut acest chec pufos cu cacao de atata ori si pentru atat de multe ocazii, incat cred ca-l pot face cu "
      "ochii inchisi. Checul este unul din deserturile clasice romanesti. Il faceau bunicile noastre, mamele noastre "
      "si acum este randul nostru sa ducem reteta mai departe. Este atat de iubit si de popular incat tuturor le "
      "place. Mama este una dintre marile iubitoarele acestui chec, la fel ca mine, de altfel. Alaturi de reteta de "
      "cozonac, checul este desertul pe care il facea cel mai des. Ni l-a facut toata copilaria si imi amintesc cu "
      "drag si nostalgie de feliile groase de chec presarate din abundenta cu zahar pudra. Era minunat pentru micul "
      "dejun, dar si ca gustare, alaturi de un pahar cu lapte sau de o cafea. Il manacam imediat si rar ne mai ramanea "
      "si a doua zi.\nReteta aceasta de chec pufos cu cacao este putin diferita de cea pe care o facea mama. Am "
      "modificat-o in asa fel incat sa fie usor de facut si sa reduc la minim riscul de a da gres. Cel mai important "
      "lucru atunci cand faceti aceasta reteta este sa bateti cat mai bine albusurile. Trebuie sa incorporati cat mai "
      "mult aer in ele. Pentru asta puteti folosi un stand-mixer sau pur si simplu un mixer manual. Puteti incerca si "
      "cu un tel, insa va dura considerabil mai mult timp. Aveti grija cand separati albusurile! Nicio picatura de "
      "galbenus nu trebuie sa ajunga in ele. La fel, nicio picatura de grasime, altfel nu se vor bate cum trebuie. Si "
      "bolul trebuie sa fie bine spalat si degresat cu putina zeama de lamaie sau otet.Evitati sa folositi boluri din "
      "plastic pentru ca nu se vor curata la fel de bine."
    ]
    warmup1 = warmup_context[:1]
    warmup4 = warmup_context + warmup_context
    self.P(f'Warming up with {len(warmup1)} texts')
    self.embed_texts(warmup_context[:1])
    self.P(f'Warming up with {len(warmup4)} texts')
    self.embed_texts(warmup_context + warmup_context)
    self.P(f'Warmup done')
    return

  """PREPROCESS OF REQUESTS"""
  if True:
    def processed_bad_request(self, msg, request_id=None, predict_kwargs=None):
      return {
        DocEmbCt.REQUEST_ID: request_id,
        DocEmbCt.REQUEST_TYPE: DocEmbCt.BAD_REQUEST,
        DocEmbCt.REQUEST_PARAMS: {},
        DocEmbCt.ERROR_MESSAGE: msg,
        'PREDICT_KWARGS': predict_kwargs or {},
      }

    """VALIDATION OF REQUESTS"""
    if True:
      def doc_embedding_valid_docs(self, docs_value):
        is_bad_request, processed_request_params, err_msg = False, {}, ""
        if not isinstance(docs_value, list) or not all([isinstance(x, str) for x in docs_value]):
          additional = ""
          if isinstance(docs_value, list):
            non_str_types = [type(x) for x in docs_value if not isinstance(x, str)]
            non_str_types = list(set(non_str_types))
            additional = f" containing non string types: {non_str_types}"
          # endif list, but not all strings
          err_msg = (f"Error! For ADD_DOC request `{DocEmbCt.REQUEST_PARAMS}` the `docs` key must be a list of strings."
                     f"Received {type(docs_value)}{additional}.")
          is_bad_request = True
        else:
          processed_request_params = {'docs': docs_value}
        # endif valid docs_value
        return is_bad_request, processed_request_params, err_msg

      def doc_embedding_valid_doc(self, doc_value):
        is_bad_request, processed_request_params, err_msg = False, {}, ""
        if not isinstance(doc_value, str):
          err_msg = (f"Error! For ADD_DOC request `{DocEmbCt.REQUEST_PARAMS}` the `doc` key must be a string."
                     f"Received {type(doc_value)}.")
          is_bad_request = True
        else:
          processed_request_params = {'docs': [doc_value]}
        # endif valid doc_value
        return is_bad_request, processed_request_params, err_msg

      def doc_embedding_valid_url(self, url_value):
        is_bad_request, processed_request_params, err_msg = False, {}, ""
        err_msg = "Error! The `url` key is not available for the moment."
        is_bad_request = True
        return is_bad_request, processed_request_params, err_msg

      def doc_embedding_validate_request_params(self, request_type, request_params):
        """
        Method for validating the request parameters.

        Parameters
        ----------
        request_type : str - the request type
        request_params : dict - the request parameters

        Returns
        -------

        is_bad_request : bool - whether the request is bad
        processed_request_params : dict - the processed request parameters
        err_msg : str - the error message if any
        """
        is_bad_request, processed_request_params, err_msg = False, {}, ""
        # Normalize the keys to lowercase.
        lowercase_params = {k.lower(): v for k, v in request_params.items()}

        if request_type == DocEmbCt.LIST_CONTEXT:
          # No additional parameters are needed
          pass
        elif request_type == DocEmbCt.QUERY:
          query_value = lowercase_params.get('query', None)
          if query_value is None or not isinstance(query_value, str):
            err_msg = (f"Error! `{DocEmbCt.REQUEST_PARAMS}` must contain a 'query' key with a string value. "
                       f"Received {type(query_value)}.")
            is_bad_request = True
          else:
            processed_request_params = {
              'query': query_value,
              'k': lowercase_params.get('k', 10)
            }
          # endif query not in request params
        elif request_type == DocEmbCt.ADD_DOC:
          doc_value = lowercase_params.get('doc', None)
          docs_value = lowercase_params.get('docs', None)
          url_value = lowercase_params.get('url', None)

          if doc_value is None and docs_value is None and url_value is None:
            err_msg = (f"Error! For ADD_DOC request `{DocEmbCt.REQUEST_PARAMS}` must contain at least "
                       f"one of {DocEmbCt.AVAILABLE_DOCS} keys. Received {list(lowercase_params.keys())}.")
            is_bad_request = True
          else:
            # At least one is present
            if docs_value is not None:
              is_bad_request, processed_request_params, err_msg = self.doc_embedding_valid_docs(docs_value)
            elif doc_value is not None:
              is_bad_request, processed_request_params, err_msg = self.doc_embedding_valid_doc(doc_value)
            elif url_value is not None:
              is_bad_request, processed_request_params, err_msg = self.doc_embedding_valid_url(url_value)
          # endif doc, docs and url are None
        else:
          # This should not happen. We already checked the request type and this is only a sanity check.
          err_msg = f"Error! `{DocEmbCt.REQUEST_TYPE}` value must be one of {DocEmbCt.REQUEST_TYPES}. Received {request_type}."
          is_bad_request = True
        # endif request_params checks
        if not is_bad_request:
          processed_request_params['context'] = lowercase_params.get('context', None)
        # endif not bad request
        return is_bad_request, processed_request_params, err_msg
    """END VALIDATION OF REQUESTS"""

    def get_additional_metadata(self):
      return {
        'MODEL_NAME': self.cfg_model_name,
        'EMBEDDING_SIZE': EMBEDDING_SIZE,
        'MAX_SEGMENT_SIZE': MAX_SEGMENT_SIZE,
        'CONTEXTS': list(self.__dbs.keys())
      }

    def _pre_process(self, inputs):
      """
      Preprocess the inputs for the prediction.
      The inputs should have the following format:
      {
        'DATA': [
          {
            # Will add doc to the default context
            'REQUEST_ID': 'request_id_1',
            'REQUEST_TYPE': 'ADD_DOC',
            'REQUEST_PARAMS': {
              'doc': 'text1',
            }
          },
          {
            # Will add docs to the default context
            'REQUEST_ID': 'request_id_2',
            'REQUEST_TYPE': 'ADD_DOC',
            'REQUEST_PARAMS': {
              'docs': ['text2', 'text3'],
            }
          },
          {
            # This is unavailable for the moment.
            # Will add the content from https://www.example.com to 'context1'
            'REQUEST_ID': 'request_id_3',
            'REQUEST_TYPE': 'ADD_DOC',
            'REQUEST_PARAMS': {
              'url': 'https://www.example.com',
              'context': 'context1',
            }
          },
          {
            # Will compute the closest 10 documents to 'query1' in the default context
            'REQUEST_ID': 'request_id_4',
            'REQUEST_TYPE': 'QUERY',
            'REQUEST_PARAMS': {
              'query': 'query1',
              'k': 10,
            }
          }
          ...
        ],
        'SERVING_PARAMS': [
          {
            'param1': 'value1',
            'param2': 'value2',
          },
          {},
          ...
        ]
      }, where SERVING_PARAMS is optional and contains additional parameters for the prediction.
      The requests can be of the following types:

      - ADD_DOC:
        The request params must contain either a 'doc' or a 'docs' key.
        The 'doc' key must have a string value representing the document to be added to the specified context.
        The 'docs' key must have a list of strings representing the documents to be added to the specified context.
        The 'url' key is unavailable for the moment.
        If both keys are present, the 'docs' key will be used.
        If no context is specified through the 'context' key in the "REQUEST_PARAMS" dict,
        the default context will be used.

      - QUERY:
        The request params must contain a 'query' key with a string value representing the query to be solved.
        The 'k' key is optional and must have an integer value representing the number of closest documents to be returned.
        If the 'k' key is not present, the default value of 10 will be used.
        Same as the 'ADD_DOC' request, the 'context' key is used to specify the context to be used.

      - LIST_CONTEXT:
        No additional parameters are needed.
        This request will return the list of available contexts.

      Parameters
      ----------
      inputs : dict - the inputs for the prediction

      Returns
      -------

      processed_requests : list[dict] - the processed requests

      """
      lst_inputs = inputs.get('DATA', [])
      serving_params = inputs.get('SERVING_PARAMS', [])
      if len(lst_inputs) == 0:
        return []
      # endif no inputs

      processed_requests = []
      for i, inp in enumerate(lst_inputs):
        is_bad_request = False
        msg = ""
        # Check if the input is a dictionary
        if not isinstance(inp, dict):
          msg = f"Error! Input {i} must be a dict. Received {type(inp)}!"
          self.P(msg)
          processed_requests.append(self.processed_bad_request(msg))
          continue
        # endif input is a string

        predict_kwargs = serving_params[i] if i < len(serving_params) else {}
        normalized_input = {k.upper(): v for k, v in inp.items()}
        request_id = normalized_input.get(DocEmbCt.REQUEST_ID, None)
        if request_id is None:
          msg = f"Warning! Request {i} must have a request id specified in `{DocEmbCt.REQUEST_ID}`."
          self.P(msg)
        # endif request_id provided

        # Check request type
        request_type = normalized_input.get(DocEmbCt.REQUEST_TYPE, DocEmbCt.DEFAULT_REQUEST_TYPE)
        if request_type not in DocEmbCt.REQUEST_TYPES:
          msg = f"Error! `{DocEmbCt.REQUEST_TYPE}` value must be one of {DocEmbCt.REQUEST_TYPES}. Received {request_type}."
          self.P(msg)
          processed_requests.append(self.processed_bad_request(msg, request_id=request_id))
          continue
        # endif request type is not valid

        # Check request params
        request_params = normalized_input.get(DocEmbCt.REQUEST_PARAMS, {})
        if not isinstance(request_params, dict) and request_type != DocEmbCt.LIST_CONTEXT:
          msg = f"Error! `{DocEmbCt.REQUEST_PARAMS}` value must be a dict. Received {type(request_params)}!"
          self.P(msg)
          processed_requests.append(self.processed_bad_request(msg, request_id=request_id))
          continue
        # endif request params is not a dict

        # Validate the request params
        is_bad_request, processed_request_params, msg = self.doc_embedding_validate_request_params(
          request_type=request_type, request_params=request_params
        )

        processed_requests.append({
          DocEmbCt.REQUEST_ID: request_id,
          DocEmbCt.REQUEST_TYPE: request_type if not is_bad_request else DocEmbCt.BAD_REQUEST,
          DocEmbCt.REQUEST_PARAMS: processed_request_params if not is_bad_request else {},
          DocEmbCt.ERROR_MESSAGE: msg,
          'PREDICT_KWARGS': predict_kwargs
        })
      # endfor each input
      return processed_requests
  """END PREPROCESS OF REQUESTS"""

  """PROCESSING OF REQUESTS"""
  if True:
    def pooling(self, last_hidden_states, attention_mask):
      """
      Pool the last hidden states using the attention mask.
      Parameters
      ----------
      last_hidden_states : torch.Tensor (batch_size, seq_len, hidden_size) with the last hidden states
      attention_mask : torch.Tensor (batch_size, seq_len) with 0s for padding and 1s for real tokens

      Returns
      -------
      torch.Tensor (batch_size, hidden_size) with the pooled embeddings
      """
      return (self.th.sum(last_hidden_states * attention_mask.unsqueeze(-1), dim=1) /
              self.th.sum(attention_mask, dim=1, keepdim=True))

    def embed_texts(self, texts):
      """
      Embed the texts using the model.
      Parameters
      ----------
      texts : str or list[str] - the text or the list of texts to be embedded

      Returns
      -------

      """
      if not isinstance(texts, list):
        texts = [texts]
      # endif texts is not a list
      if self.cfg_max_batch_size is not None and len(texts) > self.cfg_max_batch_size:
        batches = [texts[i:i + self.cfg_max_batch_size] for i in range(0, len(texts), self.cfg_max_batch_size)]
      else:
        batches = [texts]
      # endif more texts than max batch size
      embeddings = []
      for batch in batches:
        with self.th.no_grad():
          input_dict = self.tokenizer(
            batch, max_length=self.cfg_max_emb_size, padding=True, truncation=True, return_tensors='pt'
          )
          input_dict = {k: v.to(self.device) for k, v in input_dict.items()}
          outputs = self.model(**input_dict)
        # endwith no grad
        current_embeddings = self.pooling(outputs.last_hidden_state, input_dict['attention_mask'])
        current_embeddings = self.th.nn.functional.normalize(current_embeddings, p=2, dim=1)
        embeddings.append(current_embeddings.to('cpu'))
        self.th_utils.clear_cache()
      # endfor each batch
      return self.th.cat(embeddings, dim=0)

    def __add_docs(self, docs, context: str = None):
      """
      Add the documents to the context.
      Parameters
      ----------
      docs : list[str] - the list of documents
      context : str - the context name
      """
      context = self.__context_identifier(context)
      # endif context is None
      if context not in self.__dbs:
        self.__dbs[context] = HNSWVectorDB[NaeuralDoc](workspace=self.__db_cache_workspace(context))
        self.__backup_contexts()
      # endif context not in dbs
      segments = self.__doc_splitter.split_documents(docs)
      segments_embeddings = self.embed_texts(segments)
      curr_size = self.__dbs[context].num_docs()['num_docs']
      lst_docs = [
        NaeuralDoc(text=segment, embedding=emb, idx=curr_size + i)
        for i, (segment, emb) in enumerate(zip(segments, segments_embeddings))
      ]
      # TODO: maybe check for duplicates
      self.__dbs[context].index(inputs=DocList[NaeuralDoc](lst_docs))
      return

    def get_result_dict(self, request_id, docs=None, query=None, context_list=None, error_message=None, **kwargs):
      """
      Get the result dictionary.
      Parameters
      ----------
      request_id : str - the request id
      docs : list[str] - the document list
      query : str - the query
      context_list : list[str] - the list of available contexts
      error_message : str - the error message, in case of an error
      kwargs : dict - additional parameters

      Returns
      -------
      dict - the result dictionary
      """
      uppercase_kwargs = {k.upper(): v for k, v in kwargs.items()}
      return {
        DocEmbCt.REQUEST_ID: request_id,
        'DOCS': docs,
        DocEmbCt.QUERY: query,
        'CONTEXT_LIST': context_list,
        'MODEL_NAME': self.cfg_model_name,
        DocEmbCt.ERROR_MESSAGE: error_message,
        **uppercase_kwargs
      }

    def _predict(self, preprocessed_requests):
      """
      Perform the prediction using the preprocessed requests.
      For details about the requests see the `_pre_process` method.
      Parameters
      ----------
      preprocessed_requests : list[dict] - the preprocessed requests
        - each dict must have the following keys:
          - REQUEST_ID : str - the request id
          - REQUEST_TYPE : str - the request type: QUERY, ADD_DOC, LIST_CONTEXT
          - REQUEST_PARAMS : dict - the request parameters - can vary depending on the request type
        - each dict can have the following keys(they are optional):
          - PREDICT_KWARGS(not used for the moment) : dict - the prediction kwargs,
          additional parameters for the prediction

      Returns
      -------
      list[dict] - the predictions for each query or context query
        - each dict must have the following keys
          - REQUEST_ID : str - the request id
          - DOCS : list[str] - the requested documents, empty in case of ADD_DOC or LIST_CONTEXT
          - QUERY : str - the query, None if not a query
          - CONTEXT_LIST : list[str] - the list of available contexts in case of LIST_CONTEXT or None
          - MODEL_NAME : str - the model name
          - ERROR_MESSAGE : str - the error message, if any
          - additional keys can be added
      """
      results = []
      for i, req in enumerate(preprocessed_requests):
        req_id = req[DocEmbCt.REQUEST_ID]
        req_type = req[DocEmbCt.REQUEST_TYPE]
        if req_type == DocEmbCt.LIST_CONTEXT:
          results.append(
            self.get_result_dict(request_id=req_id, context_list=list(self.__dbs.keys()))
          )
        elif req_type == DocEmbCt.ADD_DOC:
          req_params = req[DocEmbCt.REQUEST_PARAMS]
          doc = req_params.get('doc', None)
          context = req_params.get('context', None)
          docs = req_params.get('docs', []) if doc is None else [doc]
          # TODO: with this implementation a context may be influenced by multiple sets of users.
          #  This can lead to a context that is not representative for any of the users.
          self.__add_docs(docs, context)
          results.append(self.get_result_dict(request_id=req_id))
        elif req_type == DocEmbCt.QUERY:
          # TODO: maybe support the following query:
          #  query + temporary context => the context will not be saved, but will be
          #  segmented and used for the query.
          req_params = req[DocEmbCt.REQUEST_PARAMS]
          query = req_params['query']
          context = req_params.get('context', None)
          context = self.__context_identifier(context)
          k = req_params.get('k', DEFAULT_NUMBER_OF_RESULTS)
          # In case the context is not available, return an error message.
          if context not in self.__dbs:
            results.append(
              self.get_result_dict(request_id=req_id, error_message=f"Error! Context {context} not found.")
            )
            continue
          # endif context not in dbs
          # Embed the query.
          query_embedding = self.embed_texts(query)
          query_doc = NaeuralDoc(text=query, embedding=query_embedding, idx=-1)
          # Search for the closest documents.
          search_results = self.__dbs[context].search(inputs=DocList[NaeuralDoc]([query_doc]), limit=k)
          # Sort the results by the index.
          result_texts = [
            res.text for res in sorted(search_results, key=lambda x: x.idx)
          ]
          results.append(
            self.get_result_dict(request_id=req_id, docs=result_texts, query=query)
          )
        elif req_type == DocEmbCt.BAD_REQUEST:
          err_msg = req[DocEmbCt.ERROR_MESSAGE]
          results.append(
            self.get_result_dict(request_id=req_id, error_message=err_msg)
          )
        # endif request type
      # endfor each preprocessed request
      return results
  """END PROCESSING OF REQUESTS"""

  def _post_process(self, preds_batch):
    return preds_batch
# endclass BaseDocEmbServing

