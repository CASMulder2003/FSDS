from functools import wraps
from pathlib import Path
def check_cache(f) -> Path:
    """
    Checks if a file exists locally before forwarding to a 'getter'
    function if it's not found.
    
    :param src: any remote file path
    :type src: str
    :param dst: any local file path
    :type dst: str
    :returns: the local file path
    :rtype: pathlib.Path
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        src  = Path(args[0])
        dest = Path(args[1])
        if dest.exists() and dest.is_file():
            print(f"{dest} found locally!")
            return(dest)
        else:
            print(f"{dest} not found, downloading!")
            return(f(src, dest))
    return wrapper

@check_cache
def get_url(src:Path, dst:Path) -> Path:
    """
    Reads a remote file (src) and writes it to a local file (dst),
    returning a Path object that is the location of the saved data.
    
    :param src: any remote file path
    :type src: pathlib.Path
    :param dst: any local file path
    :type dst: pathlib.Path
    :returns: the local file path
    :rtype: pathlib.Path
    """

    # Get the data using the urlopen function
    response = urlopen(src) 
    filedata = response.read().decode('utf-8')
     
    # Create any missing directories in dest(ination) path
    # -- os.path.join is the reverse of split (as you saw above)
    # but it doesn't work with lists... so I had to google how 
    # to use the 'splat' operator! os.makedirs creates missing 
    # directories in a path automatically.
    dst.parent.mkdir(parents=True, exist_ok=True)
     
    with dst.open(mode='w') as f:
        f.write(filedata)
         
    print(f"Data written to {dst}!")
    
    return dst