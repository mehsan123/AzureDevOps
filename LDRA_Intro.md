##### Tunnel Lighting System
Add content using the markdown widget.
- **Bold**
- *Italic*
- [Links]()

[](smallLogo.png)


**What is SmartHotel360 ?**                  
**SmartHotel360** is a fictitious smart hospitality company showcasing the future of connected travel.  
Their vision is to provide:
- Intelligent, conversational, and personalized apps and experiences to guests 
- Modern workplace experiences and smart conference rooms for business travelers
- Real-time customer and business insights for hotel managers & investors
- Unified analytics and package deal recommendations for campaign managers.

----------

**What is the intent of this demo?**          
There’s never been a better time to be a developer. Our intent with these set of reference apps and Azure backend is to show developers how to get started building the apps of the future, today!

------

**Where is the code for the SmartHotel360 applications?**                         

The entire code for the SmartHotel360 application is maintained on GitHub at https://github.com/microsoft/SmartHotel360. The build and release pipelines in this project are set to point to this repo.

--------
**How can I deploy the application to my subscription?**                  
Please follow the exercises below to deploy the "Public Web" application.

### Exercise 1: Endpoint Creation:
Service endpoints are a bundle of properties securely stored by the VSTS and is a way for VSTS to connect to the external systems or services.

Since the connections are not established during project provisioning,the endpoint - Azure Resource Manager needs to be created manually.

1. **Azure Resource Manager Service Endpoint**: Defines and secures a connection to a Microsoft Azure subscription using Service Principal Authentication (SPA).

    In the VSTS, navigate to the **Services** by clicking on the gear icon ![](images\gear.png), and click on the **+ New Service Endpoint** button. Select the **Azure Resource Manager** and  specify the  **Connection name**, select the **Subscription** from the dropdown and click on the **OK** button. Leave the **Resource Group** empty. This endpoint will be used to connect **VSTS** and **Azure**.

    You will be prompted to authorize this connection with Azure credentials. Disable pop-up blocker in your browser if you see a blank screen after clicking the **OK** button, and retry the step.

    > ***Tip***: If your subscription is not listed or to specify an existing service principal, click the link in the dialog which will switch to manual configuration mode and follow the <a href="https://blogs.msdn.microsoft.com/devops/2015/10/04/automating-azure-resource-group-deployment-using-a-service-principal-in-visual-studio-online-buildrelease-management/"> Service Principal creation </a> instructions.

    ![](images\AzureEndpoint.png)

### Step 2: Configure Release Definition

Now that the connection is established, we will manually map the Azure endpoint to release definition.

1. Navigate to release definition **PublicWebCD** under **Releases** tab, and click on **Edit**. Click on **Tasks**.

    [](images\Updaterd1.png)

    [](images\Updaterd2.png)

2. Under **CosmosDB** phase, select **Azure Deployment CosmosDB**. Update **Azure Subscription** from the dropdown.

     [](images\Updaterd3.png)

3. Repeat the above step to update **Azure Subscription** under the **Function** phase and **Web** phase. 