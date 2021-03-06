"""Generated client library for alpha_vision version v1alpha1."""
# NOTE: This file is autogenerated and should not be edited by hand.
from apitools.base.py import base_api
from googlecloudsdk.third_party.apis.alpha_vision.v1alpha1 import alpha_vision_v1alpha1_messages as messages


class AlphaVisionV1alpha1(base_api.BaseApiClient):
  """Generated client library for service alpha_vision version v1alpha1."""

  MESSAGES_MODULE = messages
  BASE_URL = u'https://alpha-vision.googleapis.com/'

  _PACKAGE = u'alpha_vision'
  _SCOPES = [u'https://www.googleapis.com/auth/cloud-platform', u'https://www.googleapis.com/auth/cloud-vision']
  _VERSION = u'v1alpha1'
  _CLIENT_ID = '1042881264118.apps.googleusercontent.com'
  _CLIENT_SECRET = 'x_Tw5K8nnjoRAqULM9PFAC2b'
  _USER_AGENT = 'x_Tw5K8nnjoRAqULM9PFAC2b'
  _CLIENT_CLASS_NAME = u'AlphaVisionV1alpha1'
  _URL_VERSION = u'v1alpha1'
  _API_KEY = None

  def __init__(self, url='', credentials=None,
               get_credentials=True, http=None, model=None,
               log_request=False, log_response=False,
               credentials_args=None, default_global_params=None,
               additional_http_headers=None, response_encoding=None):
    """Create a new alpha_vision handle."""
    url = url or self.BASE_URL
    super(AlphaVisionV1alpha1, self).__init__(
        url, credentials=credentials,
        get_credentials=get_credentials, http=http, model=model,
        log_request=log_request, log_response=log_response,
        credentials_args=credentials_args,
        default_global_params=default_global_params,
        additional_http_headers=additional_http_headers,
        response_encoding=response_encoding)
    self.productSearch_catalogs_referenceImages = self.ProductSearchCatalogsReferenceImagesService(self)
    self.productSearch_catalogs = self.ProductSearchCatalogsService(self)
    self.productSearch = self.ProductSearchService(self)

  class ProductSearchCatalogsReferenceImagesService(base_api.BaseApiService):
    """Service class for the productSearch_catalogs_referenceImages resource."""

    _NAME = u'productSearch_catalogs_referenceImages'

    def __init__(self, client):
      super(AlphaVisionV1alpha1.ProductSearchCatalogsReferenceImagesService, self).__init__(client)
      self._upload_configs = {
          }

    def Create(self, request, global_params=None):
      """Creates and returns a new `ReferenceImage` resource.

The `product_category` and `boundingPoly` fields are optional and, if used,
should both be specified.

If they are omitted, the product category and bounding polygon are inferred
by the system.

If `boundingPoly` is specified without `product_category`, `boundingPoly`
is ignored. If `product_category` is specified without `boundingPoly`, the
image border is used as the value of `boundingPoly`.

Polygons are converted into non-rotated rectangles by the system.

Possible errors:

* Returns `INVALID_ARGUMENT` if the required fields are missing or if
  fields violate their restrictions.
* Returns `FAILED_PRECONDITION` if the catalog does not exist.
* Returns `FAILED_PRECONDITION` if a product is not detected, or if
  multiple products are detected, when `product_category` and
  `boundingPoly` are not specified.

      Args:
        request: (AlphaVisionProductSearchCatalogsReferenceImagesCreateRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ReferenceImage) The response message.
      """
      config = self.GetMethodConfig('Create')
      return self._RunMethod(
          config, request, global_params=global_params)

    Create.method_config = lambda: base_api.ApiMethodInfo(
        flat_path=u'v1alpha1/productSearch/catalogs/{catalogsId}/referenceImages',
        http_method=u'POST',
        method_id=u'alpha_vision.productSearch.catalogs.referenceImages.create',
        ordered_params=[u'parent'],
        path_params=[u'parent'],
        query_params=[],
        relative_path=u'v1alpha1/{+parent}/referenceImages',
        request_field=u'referenceImage',
        request_type_name=u'AlphaVisionProductSearchCatalogsReferenceImagesCreateRequest',
        response_type_name=u'ReferenceImage',
        supports_download=False,
    )

    def Delete(self, request, global_params=None):
      """Marks a reference image for deletion. The image will remain in the catalog.
until the next time the catalog is indexed (currently daily).

The actual image files are not deleted from Google Cloud Storage.

Returns `NOT_FOUND` if the reference image does not exist.

      Args:
        request: (AlphaVisionProductSearchCatalogsReferenceImagesDeleteRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Empty) The response message.
      """
      config = self.GetMethodConfig('Delete')
      return self._RunMethod(
          config, request, global_params=global_params)

    Delete.method_config = lambda: base_api.ApiMethodInfo(
        flat_path=u'v1alpha1/productSearch/catalogs/{catalogsId}/referenceImages/{referenceImagesId}',
        http_method=u'DELETE',
        method_id=u'alpha_vision.productSearch.catalogs.referenceImages.delete',
        ordered_params=[u'name'],
        path_params=[u'name'],
        query_params=[],
        relative_path=u'v1alpha1/{+name}',
        request_field='',
        request_type_name=u'AlphaVisionProductSearchCatalogsReferenceImagesDeleteRequest',
        response_type_name=u'Empty',
        supports_download=False,
    )

    def Get(self, request, global_params=None):
      """Gets a reference image.
Returns `NOT_FOUND` if the specified image does not exist.

      Args:
        request: (AlphaVisionProductSearchCatalogsReferenceImagesGetRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ReferenceImage) The response message.
      """
      config = self.GetMethodConfig('Get')
      return self._RunMethod(
          config, request, global_params=global_params)

    Get.method_config = lambda: base_api.ApiMethodInfo(
        flat_path=u'v1alpha1/productSearch/catalogs/{catalogsId}/referenceImages/{referenceImagesId}',
        http_method=u'GET',
        method_id=u'alpha_vision.productSearch.catalogs.referenceImages.get',
        ordered_params=[u'name'],
        path_params=[u'name'],
        query_params=[],
        relative_path=u'v1alpha1/{+name}',
        request_field='',
        request_type_name=u'AlphaVisionProductSearchCatalogsReferenceImagesGetRequest',
        response_type_name=u'ReferenceImage',
        supports_download=False,
    )

    def List(self, request, global_params=None):
      """Lists reference images.

Possible errors:

* Returns `NOT_FOUND` if the catalog does not exist.
* Returns `NOT_FOUND` if there are no images associated with the specified
  product ID.

Pagination is supported. The default page size is 10 and the maximum
is 1000. Page sizes higher than 1000 will be treated as 1000.

      Args:
        request: (AlphaVisionProductSearchCatalogsReferenceImagesListRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ListReferenceImagesResponse) The response message.
      """
      config = self.GetMethodConfig('List')
      return self._RunMethod(
          config, request, global_params=global_params)

    List.method_config = lambda: base_api.ApiMethodInfo(
        flat_path=u'v1alpha1/productSearch/catalogs/{catalogsId}/referenceImages',
        http_method=u'GET',
        method_id=u'alpha_vision.productSearch.catalogs.referenceImages.list',
        ordered_params=[u'parent'],
        path_params=[u'parent'],
        query_params=[u'pageSize', u'pageToken', u'productId'],
        relative_path=u'v1alpha1/{+parent}/referenceImages',
        request_field='',
        request_type_name=u'AlphaVisionProductSearchCatalogsReferenceImagesListRequest',
        response_type_name=u'ListReferenceImagesResponse',
        supports_download=False,
    )

  class ProductSearchCatalogsService(base_api.BaseApiService):
    """Service class for the productSearch_catalogs resource."""

    _NAME = u'productSearch_catalogs'

    def __init__(self, client):
      super(AlphaVisionV1alpha1.ProductSearchCatalogsService, self).__init__(client)
      self._upload_configs = {
          }

    def Create(self, request, global_params=None):
      """Creates and returns a new catalog resource.

Note: For v1alpha1, a catalog will not be returned by `ListCatalogs` until
reference images have been added to it. Therefore it's important that you
note the catalog name
returned by the `CreateCatalog` request as it is required for adding
reference images.

      Args:
        request: (Catalog) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Catalog) The response message.
      """
      config = self.GetMethodConfig('Create')
      return self._RunMethod(
          config, request, global_params=global_params)

    Create.method_config = lambda: base_api.ApiMethodInfo(
        http_method=u'POST',
        method_id=u'alpha_vision.productSearch.catalogs.create',
        ordered_params=[],
        path_params=[],
        query_params=[],
        relative_path=u'v1alpha1/productSearch/catalogs',
        request_field='<request>',
        request_type_name=u'Catalog',
        response_type_name=u'Catalog',
        supports_download=False,
    )

    def Delete(self, request, global_params=None):
      """Permanently deletes a catalog and its reference images from the service.

The actual image files are not deleted from Google Cloud Storage.

Returns NOT_FOUND if the catalog does not exist.

      Args:
        request: (AlphaVisionProductSearchCatalogsDeleteRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Empty) The response message.
      """
      config = self.GetMethodConfig('Delete')
      return self._RunMethod(
          config, request, global_params=global_params)

    Delete.method_config = lambda: base_api.ApiMethodInfo(
        flat_path=u'v1alpha1/productSearch/catalogs/{catalogsId}',
        http_method=u'DELETE',
        method_id=u'alpha_vision.productSearch.catalogs.delete',
        ordered_params=[u'name'],
        path_params=[u'name'],
        query_params=[],
        relative_path=u'v1alpha1/{+name}',
        request_field='',
        request_type_name=u'AlphaVisionProductSearchCatalogsDeleteRequest',
        response_type_name=u'Empty',
        supports_download=False,
    )

    def DeleteReferenceImages(self, request, global_params=None):
      """Marks all reference images associated with a product for deletion.

The actual image files are not deleted from Google Cloud Storage.

Possible errors:

* Returns `INVALID_ARGUMENT` if `productId` is not specified.
* Returns `NOT_FOUND` if the catalog does not exist.
* Returns `NOT_FOUND` if the specified product ID is not associated with
  any reference images.

      Args:
        request: (AlphaVisionProductSearchCatalogsDeleteReferenceImagesRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Empty) The response message.
      """
      config = self.GetMethodConfig('DeleteReferenceImages')
      return self._RunMethod(
          config, request, global_params=global_params)

    DeleteReferenceImages.method_config = lambda: base_api.ApiMethodInfo(
        flat_path=u'v1alpha1/productSearch/catalogs/{catalogsId}/referenceImages',
        http_method=u'DELETE',
        method_id=u'alpha_vision.productSearch.catalogs.deleteReferenceImages',
        ordered_params=[u'parent'],
        path_params=[u'parent'],
        query_params=[u'productId'],
        relative_path=u'v1alpha1/{+parent}/referenceImages',
        request_field='',
        request_type_name=u'AlphaVisionProductSearchCatalogsDeleteReferenceImagesRequest',
        response_type_name=u'Empty',
        supports_download=False,
    )

    def Import(self, request, global_params=None):
      """Asynchronous API that imports a list of reference images to specified.
catalogs based on a list of image names.

This API implements the google.longrunning.Operation API allowing users
to keep track of the batch request. Progress and results can be retrieved
through the `google.longrunning.Operations` interface.
`Operation.metadata` contains `BatchOperationMetadata` describing the
progress of the operation.
`Operation.response` contains `ImportCatalogsResponse` which contains
the results.

The input source of this method is either a list of
`ImportProductSetRequest` or a CSV file on Google Cloud Storage.

The CSV file must specify one image per line. The following 5 columns
must be specified:

1. `catalog_name`
2. `image_uri`
3. `product_id`
4. `product_category`
5. `bounding_poly`

If the `catalog_id` does not exist, a new catalog will be created.

The `bounding_poly` is optional and specifies the area of interest in the
reference image. If not specified, the inferred bounding polygon is the
entire image.

      Args:
        request: (ImportCatalogsRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Operation) The response message.
      """
      config = self.GetMethodConfig('Import')
      return self._RunMethod(
          config, request, global_params=global_params)

    Import.method_config = lambda: base_api.ApiMethodInfo(
        http_method=u'POST',
        method_id=u'alpha_vision.productSearch.catalogs.import',
        ordered_params=[],
        path_params=[],
        query_params=[],
        relative_path=u'v1alpha1/productSearch/catalogs:import',
        request_field='<request>',
        request_type_name=u'ImportCatalogsRequest',
        response_type_name=u'Operation',
        supports_download=False,
    )

    def List(self, request, global_params=None):
      """Lists catalogs (in an unspecified order).

Note: Does not return empty catalogs (catalogs without reference images).

      Args:
        request: (AlphaVisionProductSearchCatalogsListRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ListCatalogsResponse) The response message.
      """
      config = self.GetMethodConfig('List')
      return self._RunMethod(
          config, request, global_params=global_params)

    List.method_config = lambda: base_api.ApiMethodInfo(
        http_method=u'GET',
        method_id=u'alpha_vision.productSearch.catalogs.list',
        ordered_params=[],
        path_params=[],
        query_params=[],
        relative_path=u'v1alpha1/productSearch/catalogs',
        request_field='',
        request_type_name=u'AlphaVisionProductSearchCatalogsListRequest',
        response_type_name=u'ListCatalogsResponse',
        supports_download=False,
    )

  class ProductSearchService(base_api.BaseApiService):
    """Service class for the productSearch resource."""

    _NAME = u'productSearch'

    def __init__(self, client):
      super(AlphaVisionV1alpha1.ProductSearchService, self).__init__(client)
      self._upload_configs = {
          }
