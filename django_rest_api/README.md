# Django REST Framework (DRF), APIView, ModelViewSet, and GenericViewSet

## 1. APIView
### What It Is:
- APIView is the most basic class-based view in DRF. It provides the foundation for building custom API views. It doesn't include any behavior for handling common HTTP methods like GET, POST, PUT, DELETE, etc., so you must define them explicitly.

### When to Use:
- Use APIView when you need full control over the request handling process and want to customize the behavior of your API.
- Ideal for cases where you want to handle complex logic that doesn't fit neatly into the standard CRUD operations.
### Example:
```
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class CustomAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # Custom logic for GET request
        data = {"message": "Hello, GET request!"}
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        # Custom logic for POST request
        data = {"message": "Hello, POST request!"}
        return Response(data, status=status.HTTP_201_CREATED)
```

## 2. ModelViewSet
### What It Is:
- ModelViewSet is a specialized subclass of ViewSet that provides CRUD operations (Create, Retrieve, Update, Delete) out-of-the-box for a model. It handles actions like .list(), .create(), .retrieve(), .update(), and .destroy() automatically based on the model.

### When to Use:
- Use ModelViewSet when you need to quickly create a full set of CRUD API endpoints for a model, with minimal customization.
- Ideal for standard CRUD operations where the default behavior provided by DRF is sufficient.
### Example:
```
from rest_framework import viewsets
from myapp.models import MyModel
from myapp.serializers import MyModelSerializer

class MyModelViewSet(viewsets.ModelViewSet):
    queryset = MyModel.objects.all()
    serializer_class = MyModelSerializer
Routing: With ModelViewSet, you can automatically generate URL routes using a router.
python
Copy code
from rest_framework.routers import DefaultRouter
from myapp.views import MyModelViewSet

router = DefaultRouter()
router.register(r'mymodel', MyModelViewSet)

urlpatterns = router.urls
```

## 3. GenericViewSet
### What It Is:
- GenericViewSet is a base class that combines the behavior of APIView and mixins to allow you to create a viewset with a subset of the standard actions (like list, create, retrieve, update, destroy).
- Unlike ModelViewSet, it doesn't automatically provide all CRUD actions—you have to add them manually via mixins or by defining custom methods.

### When to Use:
- Use GenericViewSet when you need a viewset with only specific actions and want more control over which operations are available.
- Ideal for scenarios where you need some CRUD operations but not all, or when you want to mix custom logic with standard actions.
### Example:
```
from rest_framework import viewsets, mixins
from myapp.models import MyModel
from myapp.serializers import MyModelSerializer

class MyModelGenericViewSet(mixins.ListModelMixin,
                            mixins.RetrieveModelMixin,
                            viewsets.GenericViewSet):
    queryset = MyModel.objects.all()
    serializer_class = MyModelSerializer
```
- Routing: Similar to ModelViewSet, you can generate URL routes using a router.
```
from rest_framework.routers import DefaultRouter
from myapp.views import MyModelGenericViewSet

router = DefaultRouter()
router.register(r'mymodel', MyModelGenericViewSet)

urlpatterns = router.urls
```

### Comparison and Use Cases
Class	
- `APIView`	

CRUD Actions Provided	
- None (fully custom)	

Flexibility	
- High	

When to Use
- When you need full control and custom behavior.

Class	
- `ModelViewSet`	

CRUD Actions Provided	
- All (list, create, retrieve, update, destroy)	

Flexibility	
- Low	

When to Use
- When you want to quickly create a full CRUD API.

Class	
- `GenericViewSet`	

CRUD Actions Provided	
- None (use with mixins)	

Flexibility	
- Medium	

When to Use
- When you need some CRUD actions with additional control.


# Usage:  docker [OPTIONS] COMMAND

A self-sufficient runtime for containers

Common Commands:
- run         Create and run a new container from an image
- exec        Execute a command in a running container
- ps          List containers
- build       Build an image from a Dockerfile
- pull        Download an image from a registry
- push        Upload an image to a registry
- images      List images
- login       Log in to a registry
- logout      Log out from a registry
- search      Search Docker Hub for images
- version     Show the Docker version information
- info        Display system-wide information

Management Commands:
- builder     Manage builds
- buildx*     Docker Buildx
- compose*    Docker Compose
- container   Manage containers
- context     Manage contexts
- debug*      Get a shell into any image or container
- desktop*    Docker Desktop commands (Alpha)
- dev*        Docker Dev Environments
- extension*  Manages Docker extensions
- feedback*   Provide feedback, right in your terminal!
- image       Manage images
- init*       Creates Docker-related starter files for your project
- manifest    Manage Docker image manifests and manifest lists
- network     Manage networks
- plugin      Manage plugins
- sbom*       View the packaged-based Software Bill Of Materials (SBOM) for an image
- scout*      Docker Scout
- system      Manage Docker
- trust       Manage trust on Docker images
- volume      Manage volumes

Swarm Commands:
- swarm       Manage Swarm

Commands:
- attach      Attach local standard input, output, and error streams to a running container
- commit      Create a new image from a container's changes
- cp          Copy files/folders between a container and the local filesystem
- create      Create a new container
- diff        Inspect changes to files or directories on a container's filesystem
- events      Get real time events from the server
- export      Export a container's filesystem as a tar archive
- history     Show the history of an image
- import      Import the contents from a tarball to create a filesystem image
- inspect     Return low-level information on Docker objects
- kill        Kill one or more running containers
- load        Load an image from a tar archive or STDIN
- logs        Fetch the logs of a container
- pause       Pause all processes within one or more containers
- port        List port mappings or a specific mapping for the container
- rename      Rename a container
- restart     Restart one or more containers
- rm          Remove one or more containers
- rmi         Remove one or more images
- save        Save one or more images to a tar archive (streamed to STDOUT by default)
- start       Start one or more stopped containers
- stats       Display a live stream of container(s) resource usage statistics
- stop        Stop one or more running containers
- tag         Create a tag TARGET_IMAGE that refers to SOURCE_IMAGE
- top         Display the running processes of a container
- unpause     Unpause all processes within one or more containers
- update      Update configuration of one or more containers
- wait        Block until one or more containers stop, then print their exit codes