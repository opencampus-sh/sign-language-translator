#!/bin/bash

# Configuration
BUCKETS=(
    "sign-lang-training-data-dev"
    "sign-lang-models-dev"
    "sign-lang-evaluation-dev"
)

# Role mappings
VIEWER_ROLE="roles/storage.objectViewer"
WRITER_ROLE="roles/storage.objectUser"
ADMIN_ROLE="roles/storage.admin"

usage() {
    echo "Usage: $0 <action> <email> [role]"
    echo "Actions: add, remove, list"
    echo "Roles: viewer, writer, admin"
    echo ""
    echo "Examples:"
    echo "  $0 add john@company.com viewer"
    echo "  $0 remove john@company.com writer"
    echo "  $0 list"
    exit 1
}

get_role() {
    local role_type=$1
    case $role_type in
        "viewer") echo $VIEWER_ROLE ;;
        "writer") echo $WRITER_ROLE ;;
        "admin") echo $ADMIN_ROLE ;;
        *) echo "Invalid role type. Use: viewer, writer, or admin"; exit 1 ;;
    esac
}

add_access() {
    local email=$1
    local role_type=$2
    local role=$(get_role $role_type)

    echo "Adding $email with role $role to all buckets..."
    for bucket in "${BUCKETS[@]}"; do
        echo "Processing bucket: gs://$bucket"
        gcloud storage buckets add-iam-policy-binding "gs://$bucket" \
            --member="user:$email" \
            --role="$role"
    done
}

remove_access() {
    local email=$1
    local role_type=$2
    local role=$(get_role $role_type)

    echo "Removing $email with role $role from all buckets..."
    for bucket in "${BUCKETS[@]}"; do
        echo "Processing bucket: gs://$bucket"
        gcloud storage buckets remove-iam-policy-binding "gs://$bucket" \
            --member="user:$email" \
            --role="$role"
    done
}

list_access() {
    echo "Current permissions for all buckets:"
    for bucket in "${BUCKETS[@]}"; do
        echo -e "\nBucket: gs://$bucket"
        echo "----------------------------------------"
        gcloud storage buckets get-iam-policy "gs://$bucket" \
            --format="table(bindings.members,bindings.role)"
    done
}

verify_email() {
    local email=$1
    if [[ ! $email =~ ^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$ ]]; then
        echo "Invalid email format"
        exit 1
    fi
}

# Main script
case $1 in
    "add")
        if [ "$#" -ne 3 ]; then usage; fi
        verify_email $2
        add_access $2 $3
        ;;
    "remove")
        if [ "$#" -ne 3 ]; then usage; fi
        verify_email $2
        remove_access $2 $3
        ;;
    list")

        list_access
        ;;
    *)
        usage
        ;;
esac
