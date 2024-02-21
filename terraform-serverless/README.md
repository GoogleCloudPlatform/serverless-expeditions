# My cat photo identification service

To deploy using Terraform:

 * Create a new project on Google Cloud with [billing enabled](https://cloud.google.com/billing/docs/how-to/modify-project), and launch [Cloud Shell](https://cloud.google.com/shell/docs/using-cloud-shell).
 * Clone this repo (or open automatically in [Cloud Shell][shell_link])

    ```shell
    git clone https://github.com/GoogleCloudPlatform/serverless-expeditions 
    cd serverless-expeditions/terraform-serverless
    ```

  * Build the base service container:

    ```
    gcloud builds submit
    ```
  * Assuming you are using cloudshell. You need to set up cloudshell Role as the following steps:
    1. Go to the IAM & Admin page in the Google Cloud Console.
    1. Find the Compute Engine default service account in the list. This is usually in the format of YOUR_NUMBER-compute@developer.gserviceaccount.com.
    1. Click on the pencil icon to edit the service account.
    1.  Click on Add Another Role.
    1. In the Select a role dropdown, search for ‘Create Service Accounts.
    1.  Click on Save to save your changes.
  * Initialize and apply the Terraform manifests: 

    ```
    terraform init
    terraform apply
    ```

See [docs/](docs/) for more details of this demo. 


## Learn more

 * [Managing Infrastructure as Code](https://cloud.google.com/solutions/managing-infrastructure-as-code)
 * [Processing images from Cloud Storage tutorial ](https://cloud.google.com/run/docs/tutorials/image-processing)


[shell_img]: http://gstatic.com/cloudssh/images/open-btn.png
[shell_link]: https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/serverless-expeditions&page=editor&open_in_editor=terraform-serverless/README.md
