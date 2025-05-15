# DuploCloud Resource Provider

The DuploCloud Resource Provider lets you manage [DuploCloud](https://duplocloud.com/) resources.

## Installing

This package is available for several languages/platforms:

### Node.js (JavaScript/TypeScript)

To use from JavaScript or TypeScript in Node.js, install using either `npm`:

```bash
npm install @duplocloud/pulumi
```

or `yarn`:

```bash
yarn add @duplocloud/pulumi
```

### Python

To use from Python, install using `pip`:

```bash
pip install pulumi-duplocloud
```

### Go

To use from Go, use `go get` to grab the latest version of the library:

```bash
go get github.com/duplocloud/pulumi-duplocloud/sdk/go/...
```


## Configuration

The DuploCloud provider requires the following configuration parameters:

- `duplocloud:duploHost` - Base URL to the DuploCloud REST API
- `duplocloud:duploToken` - Bearer token for authentication

You can set these using environment variables:

```bash
export duplo_host="https://your-duplocloud-instance.com"
export duplo_token="<your_duplo_token>"
```

## Example usage

### Go

```golang
package main

import (
	"github.com/duplocloud/pulumi-duplocloud/sdk/go/duplocloud"
	"github.com/pulumi/pulumi/sdk/v3/go/pulumi"
)

func main() {
	pulumi.Run(func(ctx *pulumi.Context) error {
		// Set up the infrastructure.

		infra, err := duplocloud.NewInfrastructure(ctx, "infra", &duplocloud.InfrastructureArgs{
			InfraName:       pulumi.String("pulumi-infra"),
			Cloud:           pulumi.Int(0),
			Region:          pulumi.String("us-east-2"),
			Azcount:         pulumi.Int(2),
			SubnetCidr:      pulumi.Int(24),
			EnableK8Cluster: pulumi.Bool(true),
			AddressPrefix:   pulumi.String("10.22.0.0/16"),
		})
		if err != nil {
			return err
		}
		ctx.Export("infraName", infra.InfraName)
		ctx.Export("vpcId", infra.VpcId)

		// Create DuploCloud Tenant
		tenant, err := duplocloud.NewTenant(ctx, "dev", &duplocloud.TenantArgs{
			AccountName:   pulumi.String("dev"),
			PlanId:        infra.InfraName,
			AllowDeletion: pulumi.Bool(true),
		}, pulumi.DependsOn([]pulumi.Resource{infra}))
		if err != nil {
			return err
		}
		ctx.Export("tenantId", tenant.ID())

		// Get native image
		image := duplocloud.GetNativeHostImageOutput(ctx, duplocloud.GetNativeHostImageOutputArgs{
			TenantId:     tenant.TenantId,
			IsKubernetes: pulumi.Bool(true),
		}, nil)

		// Create EKS Node
		node, err := duplocloud.NewAwsHost(ctx, "node", &duplocloud.AwsHostArgs{
			TenantId:      tenant.TenantId,
			FriendlyName:  pulumi.String("node01"),
			ImageId:       image.ImageId(),
			Capacity:      pulumi.String("t3a.medium"),
			AgentPlatform: pulumi.Int(7),
			Zone:          pulumi.Int(0),
			Metadatas: duplocloud.AwsHostMetadataArray{
				&duplocloud.AwsHostMetadataArgs{
					Key:   pulumi.String("OsDiskSize"),
					Value: pulumi.String("20"),
				},
			},
		}, pulumi.DependsOn([]pulumi.Resource{tenant, infra}))
		if err != nil {
			return err
		}

		// Create a service
		webapp, err := duplocloud.NewDuploService(ctx, "web-app", &duplocloud.DuploServiceArgs{
			TenantId:      tenant.TenantId,
			Name:          pulumi.String("web-app"),
			AgentPlatform: pulumi.Int(7),
			DockerImage:   pulumi.String("nginx:latest"),
			Replicas:      pulumi.Int(1),
		}, pulumi.DependsOn([]pulumi.Resource{node, tenant, infra}))
		if err != nil {
			return err
		}

		// Configure Load Balancer
		cert_arn := "arn:aws:acm:us-east-1:1234567890:certificate/d6c4138f-583e-4c75-a314-851142670b64"
		_, err = duplocloud.NewDuploServiceLbconfigs(ctx, "web-app-lb", &duplocloud.DuploServiceLbconfigsArgs{
			TenantId:                  webapp.TenantId,
			ReplicationControllerName: webapp.Name,
			Lbconfigs: duplocloud.DuploServiceLbconfigsLbconfigArray{
				&duplocloud.DuploServiceLbconfigsLbconfigArgs{
					ExternalPort:   pulumi.Int(443),
					HealthCheckUrl: pulumi.String("/"),
					IsNative:       pulumi.Bool(false),
					LbType:         pulumi.Int(1),
					Port:           pulumi.String("80"),
					Protocol:       pulumi.String("http"),
					CertificateArn: pulumi.String(cert_arn),
					HealthCheck: &duplocloud.DuploServiceLbconfigsLbconfigHealthCheckArgs{
						HealthyThreshold:   pulumi.Int(4),
						UnhealthyThreshold: pulumi.Int(4),
						Timeout:            pulumi.Int(50),
						Interval:           pulumi.Int(30),
						HttpSuccessCodes:   pulumi.String("200-399"),
					},
				},
			},
		}, pulumi.DependsOn([]pulumi.Resource{webapp, node, tenant, infra}))
		if err != nil {
			return err
		}
		return nil
	})
}
```

### Python

```python
import pulumi
import pulumi_duplocloud as duplo

# Create DuploCloud Infrastructure
infra = duplo.infrastructure.Infrastructure(resource_name="pulumi-infra",
    infra_name="pulumi-infra",
    cloud=0,
    region="us-east-2",
    azcount=2,
    subnet_cidr=24,
    address_prefix="10.22.0.0/16",
    enable_k8_cluster=True,  # Enable Kubernetes
)

# Export the outputs
pulumi.export("vpc_id", infra.vpc_id)

# Create Tenant
tenant = duplo.tenant.Tenant(resource_name="dev",
    account_name="dev",
    plan_id=infra.infra_name,
)

# Export the outputs
pulumi.export("tenantId", tenant.tenant_id)

# Create EKS Node
image = duplo.get_native_host_image_output(tenant_id=tenant.tenant_id,
            is_kubernetes=True)

node = duplo.AwsHost(resource_name="Node01",
    tenant_id=tenant.tenant_id,
    friendly_name="Node01",
    image_id=image.image_id,
    capacity="t3a.medium",
    agent_platform=7,
    zone=0,
    metadatas=[{
        "key": "OsDiskSize",
        "value": "20",
    }]
)

# Deploy nginx service on EKS

cert_arn="arn:aws:acm:us-east-1:1234567890:certificate/d6c4138f-583e-4c75-a314-851142670b64"
app_service = duplo.duplo_service.DuploService(resource_name="web-application",
    opts=pulumi.ResourceOptions(depends_on=[node]),
    tenant_id=tenant.tenant_id,
    name="web-app",
    docker_image="nginx:latest",
    replicas=1,
    agent_platform=7,
)

# Configure Load Balancer
app_lbconfigs = duplo.DuploServiceLbconfigs(resource_name="web-application-lb",
    tenant_id=tenant.tenant_id,
    replication_controller_name=app_service.name,
    lbconfigs=[{
        "external_port": 443,
        "health_check_url": "/",
        "is_native": False,
        "lb_type": 1,
        "port": "80",
        "protocol": "http",
        "certificate_arn":  cert_arn,
        "health_check": {
            "healthy_threshold": 4,
            "unhealthy_threshold": 4,
            "timeout": 10,
            "interval": 30,
            "http_success_codes": "200-399",
        },
    }]
)

```

### TypeScript

```typescript
import * as duplocloud from "@duplocloud/pulumi";

const certArn = "arn:aws:acm:us-east-1:1234567890:certificate/d6c4138f-583e-4c75-a314-851142670b64"

// Create DuploCloud infrastructure
const infra = new duplocloud.Infrastructure("infra", {
    infraName: "pulumi-infra",
    cloud: 0,
    region: "us-east-2",
    azcount: 2,
    subnetCidr: 24,
    enableK8Cluster: true,
    addressPrefix: "10.22.0.0/16",
});

export const vpcId = infra.vpcId;

// Create DuploCloud tenant
const tenant = new duplocloud.Tenant("dev", {
    accountName: "dev",
    planId: infra.infraName,
}, { dependsOn: [infra] });

export const tenantId = tenant.tenantId;

const image = duplocloud.getNativeHostImageOutput({
    tenantId: tenant.tenantId,
    isKubernetes: true,
});

// Create DuploCloud node
const node = new duplocloud.AwsHost("Node01", {
    tenantId: tenant.tenantId,
    friendlyName: "Node01",
    imageId: image.imageId,
    capacity: "t3a.medium",
    agentPlatform: 7,
    zone: 0,
    metadatas: [{
        key: "OsDiskSize",
        value: "20",
    }],
}, { dependsOn: [tenant] });

// Create DuploCloud service
const app_service = new duplocloud.DuploService("web-application", {
    tenantId: tenant.tenantId,
    name: "web-app",
    agentPlatform: 7,
    dockerImage: "nginx:latest",
    replicas: 1,
}, { dependsOn: [node] });

// Create DuploCloud load balancer
const appLbconfigs = new duplocloud.DuploServiceLbconfigs("web-application-lbconfigs", {
    tenantId: app_service.tenantId,
    replicationControllerName: app_service.name,
    lbconfigs: [{
        externalPort: 80,
        healthCheckUrl: "/",
        isNative: false,
        lbType: 1,
        port: "80",
        protocol: "http",
        certificateArn: certArn,
        healthCheck: {
            healthyThreshold: 4,
            unhealthyThreshold: 4,
            timeout: 50,
            interval: 30,
            httpSuccessCodes: "200-399",
        },
    }],
});
```
