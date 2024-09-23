@echo off
setlocal

rem Set the path to your QNX6 dependencies
set QNX6_DEPENDENCIES="qemu-nbd qnx6mount"

rem Path to the QNX6 .bin file (you can modify this to accept user input)
set BIN_IMAGE_PATH=C:\path\to\your\image.bin
set MOUNT_BASE_DIR=/mnt/c/path/to/mount/dir

rem Start WSL and check for dependencies
wsl -e bash -c "
    echo 'Checking for dependencies...';
    missing_deps=();
    for dep in $QNX6_DEPENDENCIES; do
        if ! command -v \$dep &> /dev/null; then
            missing_deps+=(\$dep);
        fi
    done;

    if [ \${#missing_deps[@]} -ne 0 ]; then
        echo 'The following dependencies are missing: \${missing_deps[@]}';
        echo 'Installing missing dependencies...';
        sudo apt update;
        sudo apt install -y \${missing_deps[@]};
    else
        echo 'All dependencies are installed.';
    fi

    echo 'Mounting QNX6 image...';
    if [ ! -f $BIN_IMAGE_PATH ]; then
        echo 'Error: QNX6 image not found at $BIN_IMAGE_PATH.';
        exit 1;
    fi
    
    echo 'Attaching the image as an NBD device...';
    sudo qemu-nbd -c /dev/nbd0 $BIN_IMAGE_PATH;

    echo 'Identifying partitions...';
    fdisk_output=\$(sudo fdisk -l /dev/nbd0);
    echo \$fdisk_output;

    partition_pattern='(/dev/nbd0p[0-9]+)';
    partitions=(\$(echo \$fdisk_output | grep -oP \"\$partition_pattern\"));

    if [ \${#partitions[@]} -eq 0 ]; then
        echo 'No partitions found.';
        exit 1;
    fi

    for partition in \"\${partitions[@]}\"; do
        mount_point='$MOUNT_BASE_DIR/\$(basename \$partition)';
        mkdir -p \$mount_point;
        echo 'Mounting \$partition to \$mount_point...';
        sudo qnx6mount \$partition \$mount_point && echo 'Mounted successfully.' || echo 'Failed to mount.';
    done;

    echo 'Detaching the NBD device...';
    sudo qemu-nbd -d /dev/nbd0;
"

rem Optional: Launch a GUI file explorer to the mount point
start explorer.exe C:\path\to\mount\dir

endlocal
