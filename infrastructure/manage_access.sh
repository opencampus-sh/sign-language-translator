#!/bin/bash

# Import variables from terraform.tfvars
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TFVARS_FILE="$SCRIPT_DIR/../terraform/environments/dev/terraform.tfvars"

if [ ! -f "$TFVARS_FILE" ]; then
    echo "Error: terraform.tfvars not found at $TFVARS_FILE"
    exit 1
fi

# Parse project_id from terraform.tfvars
PROJECT_ID=$(grep 'project_id' "$TFVARS_FILE" | cut -d'=' -f2 | tr -d '" ' )

# Configuration
BUCKETS=(
    "${PROJECT_ID}-training-data-dev"
)

# Role mappings
declare -A STORAGE_ROLES=(
    ["viewer"]="roles/storage.objectViewer"
    ["writer"]="roles/storage.objectUser"
    ["admin"]="roles/storage.admin"
)

declare -A VERTEX_ROLES=(
    ["viewer"]="roles/aiplatform.viewer"
    ["user"]="roles/aiplatform.user"
    ["admin"]="roles/aiplatform.admin"
    ["job_user"]="roles/aiplatform.customJobUser"
    ["model_user"]="roles/aiplatform.modelUser"
    ["endpoint_deployer"]="roles/aiplatform.endpointDeployer"
)

usage() {
    echo "Usage: $0 <action> <email> [role] [service]"
    echo "Actions: add, remove, list"
    echo "Roles for storage: viewer, writer, admin"
    echo "Roles for vertex:"
    echo "  - viewer: Can view resources"
    echo "  - user: Full access to use Vertex AI"
    echo "  - admin: Full administrative access"
    echo "  - job_user: Can run custom jobs"
    echo "  - model_user: Can use model endpoints"
    echo "  - endpoint_deployer: Can deploy endpoints"
    echo "Services: storage (default), vertex, all"
    echo ""
    echo "Examples:"
    echo "  $0 add john@company.com job_user vertex"
    echo "  $0 add jane@company.com model_user vertex"
    echo "  $0 add bob@company.com endpoint_deployer vertex"
    exit 1
}

get_storage_role() {
    local role_type=$1
    local role=${STORAGE_ROLES[$role_type]}
    if [ -z "$role" ]; then
        echo "Invalid storage role type. Use: viewer, writer, or admin"
        exit 1
    fi
    echo $role
}

get_vertex_role() {
    local role_type=$1
    local role=${VERTEX_ROLES[$role_type]}
    if [ -z "$role" ]; then
        echo "Invalid vertex role type. Use: viewer, user, or admin"
        exit 1
    fi
    echo $role
}

add_storage_access() {
    local email=$1
    local role_type=$2
    local role=$(get_storage_role $role_type)

    echo "Adding $email with role $role to all buckets..."
    for bucket in "${BUCKETS[@]}"; do
        echo "Processing bucket: gs://$bucket"
        gcloud storage buckets add-iam-policy-binding "gs://$bucket" \
            --member="user:$email" \
            --role="$role"
    done
}

add_vertex_access() {
    local email=$1
    local role_type=$2
    local role=$(get_vertex_role $role_type)

    echo "Adding $email with role $role to Vertex AI..."
    gcloud projects add-iam-policy-binding $PROJECT_ID \
        --member="user:$email" \
        --role="$role"
}

remove_storage_access() {
    local email=$1
    local role_type=$2
    local role=$(get_storage_role $role_type)

    echo "Removing $email with role $role from all buckets..."
    for bucket in "${BUCKETS[@]}"; do
        echo "Processing bucket: gs://$bucket"
        gcloud storage buckets remove-iam-policy-binding "gs://$bucket" \
            --member="user:$email" \
            --role="$role"
    done
}

remove_vertex_access() {
    local email=$1
    local role_type=$2
    local role=$(get_vertex_role $role_type)

    echo "Removing $email with role $role from Vertex AI..."
    gcloud projects remove-iam-policy-binding $PROJECT_ID \
        --member="user:$email" \
        --role="$role"
}

list_access() {
    echo "Current storage permissions for all buckets:"
    for bucket in "${BUCKETS[@]}"; do
        echo -e "\nBucket: gs://$bucket"
        echo "----------------------------------------"
        gcloud storage buckets get-iam-policy "gs://$bucket" \
            --format="table(bindings.members,bindings.role)"
    done

    echo -e "\nCurrent Vertex AI permissions:"
    echo "----------------------------------------"
    gcloud projects get-iam-policy $PROJECT_ID \
        --format="table(bindings.members,bindings.role)" \
        --filter="bindings.role:aiplatform"
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
        if [ "$#" -lt 3 ]; then usage; fi
        verify_email $2
        service=${4:-"storage"}  # Default to storage if not specified
        
        case $service in
            "storage")
                add_storage_access $2 $3
                ;;
            "vertex")
                add_vertex_access $2 $3
                ;;
            "all")
                add_storage_access $2 $3
                add_vertex_access $2 $3
                ;;
            *)
                echo "Invalid service. Use: storage, vertex, or all"
                exit 1
                ;;
        esac
        ;;
    "remove")
        if [ "$#" -lt 3 ]; then usage; fi
        verify_email $2
        service=${4:-"storage"}  # Default to storage if not specified
        
        case $service in
            "storage")
                remove_storage_access $2 $3
                ;;
            "vertex")
                remove_vertex_access $2 $3
                ;;
            "all")
                remove_storage_access $2 $3
                remove_vertex_access $2 $3
                ;;
            *)
                echo "Invalid service. Use: storage, vertex, or all"
                exit 1
                ;;
        esac
        ;;
    "list")
        list_access
        ;;
    *)
        usage
        ;;
esac
