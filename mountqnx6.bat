@echo off
setlocal

rem Get the action (mount or unmount) and arguments from the Python script
set ACTION=%1
set BIN_IMAGE_PATH=%2
set MOUNT_BASE_DIR=%3
set SUDO_PASSWORD=%4

rem Set the path to your QNX6 dependencies
set QNX6_DEPENDENCIES="qemu-nbd qnx6mount"

if "%ACTION%" == "mount" (
    rem Mount the QNX6 image

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
            echo %SUDO_PASSWORD% | sudo -S apt update;
            echo %SUDO_PASSWORD% | sudo -S apt install -y \${missing_deps[@]};
        else
            echo 'All dependencies are installed.';
        fi

        echo 'Mounting QNX6 image...';
        if [ ! -f \"$BIN_IMAGE_PATH\" ]; then
            echo 'Error: QNX6 image not found at \"$BIN_IMAGE_PATH\".';
            exit 1;
        fi

        echo 'Attaching the image as an NBD device...';
        echo %SUDO_PASSWORD% | sudo -S qemu-nbd -c /dev/nbd0 \"$BIN_IMAGE_PATH\";

        echo 'Identifying partitions...';
        fdisk_output=\$(echo %SUDO_PASSWORD% | sudo -S fdisk -l /dev/nbd0);
        echo \$fdisk_output;

        partition_pattern='(/dev/nbd0p[0-9]+)';
        partitions=(\$(echo \$fdisk_output | grep -oP \"\$partition_pattern\"));

        if [ \${#partitions[@]} -eq 0 ]; then
            echo 'No partitions found.';
            exit 1;
        fi

        for partition in \"\${partitions[@]}\"; do
            mount_point=\"$MOUNT_BASE_DIR/\$(basename \$partition)\";
            mkdir -p \$mount_point;
            echo 'Mounting \$partition to \$mount_point...';
            echo %SUDO_PASSWORD% | sudo -S qnx6mount \$partition \$mount_point && echo 'Mounted successfully.' || echo 'Failed to mount.';
        done;

        echo 'Detaching the NBD device...';
        echo %SUDO_PASSWORD% | sudo -S qemu-nbd -d /dev/nbd0;
    "
) else if "%ACTION%" == "unmount" (
    rem Unmount the QNX6 image

    wsl -e bash -c "
        echo 'Unmounting all partitions from the mount point...';
        for mount_point in \"$MOUNT_BASE_DIR\"/*; do
            echo %SUDO_PASSWORD% | sudo -S umount \$mount_point && echo 'Unmounted successfully.' || echo 'Failed to unmount.';
            rm -rf \$mount_point;
        done;

        echo 'Detaching the NBD device...';
        echo %SUDO_PASSWORD% | sudo -S qemu-nbd -d /dev/nbd0;
    "
)

rem Optional: Launch a GUI file explorer to the mount point
if "%ACTION%" == "mount" (
    start explorer.exe "%MOUNT_BASE_DIR%"
)

endlocal
