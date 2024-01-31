async function openVm(templateId) {
    try {
        var output = await checkIfVmAlive(templateId);
        if (output == 1) {
            redirectToVmViewer(templateId);
        }
    } catch (error) {
        alert(error);
    }
}

async function deleteVm(templateId) {
    try {
        var output = await checkIfVmAlive(templateId);
        if (output == 1) {
            showLoadingModal();
            $.ajax({
                type: 'DELETE',
                url: 'https://api.insa-cvl.com/vm/delete',
                contentType: 'application/json;charset=UTF-8',
                data: JSON.stringify({ template_id: templateId }),
                xhrFields: {
                    withCredentials: true
                },
                success: function (response) {
                    hideLoadingModal();
                    location.reload();
                },
                error: function (error) {
                    alert('Erreur de suppression de la VM');
                    hideLoadingModal(); 
                }
            });
        }
    } catch (error) {
        alert(error);
        hideLoadingModal(); 
    }
}

async function getVmStatus(templateId) {
    try {
        var output = await checkIfVmAlive(templateId);
        updateButtons(templateId, output);
    } catch (error) {
        alert(error);
    }
}

function updateButtons(templateId, isVmAlive) {
    var templateCard = $('#' + templateId);

    templateCard.find("#start_vm_btn, #open_vm_btn, #open_vm_btn_new_tab, #delete_vm_btn").remove();

    var cardBody = templateCard.find(".card-body");

    if (isVmAlive == 1) {
        var openVmBtn = $('<button>').attr({
            'id': 'open_vm_btn',
            'type': 'button',
            'class': 'btn btn-success mr-1'
        }).on('click', function () {
            window.location = "/viewer?templateId=" + encodeURIComponent(templateId);
        }).text('Ouvrir');

        var openVmBtnNewTab = $('<button>').attr({
            'id': 'open_vm_btn_new_tab',
            'type': 'button',
            'class': 'btn btn-success'
        }).on('click', function () {
            window.open("/viewer?templateId=" + encodeURIComponent(templateId));
        }).html('<i class="bi bi-box-arrow-up-right"></i>');

        var buttonContainer = $('<div>').addClass('d-inline-flex');
        buttonContainer.append(openVmBtn, openVmBtnNewTab);

        var deleteBtn = $('<button>').attr({
            'id': 'delete_vm_btn',
            'type': 'button',
            'class': 'btn btn-danger'
        }).on('click', function () {
            deleteVm(templateId);
        }).text('Supprimer');

        cardBody.append(buttonContainer, $('<div>').css('margin-top', '10px'), deleteBtn);
    } else {
        var startVmBtn = $('<button>').attr({
            'id': 'start_vm_btn',
            'type': 'button',
            'class': 'btn btn-light'
        }).on('click', function () {
            createVmFromTemplate(templateId);
        }).text('Démarrer');

        cardBody.append(startVmBtn);
    }
}


async function createVmFromTemplate(templateId) {
    showLoadingModal(); 
    $.ajax({
        type: 'POST',
        url: 'https://api.insa-cvl.com/vm/create',
        contentType: 'application/json;charset=UTF-8',
        data: JSON.stringify({ template_id: templateId }),
        xhrFields: {
            withCredentials: true
        },
        success: async function (response) {
            try {
                var output = await checkIfVmAlive(templateId);
                while (output !== 1) {
                    await new Promise(resolve => setTimeout(resolve, 60000));
                    output = await checkIfVmAlive(templateId);
                }
            } catch (error) {
                alert(error);
                hideLoadingModal(); 
            }
            hideLoadingModal(); 
            location.reload();
        },
        error: function (error) {
            alert('Erreur de création de la VM');
            hideLoadingModal(); 
        }
    });
}

function redirectToVmViewer(templateId) {
    showLoadingModal();
    $.ajax({
        type: 'GET',
        url: 'https://api.insa-cvl.com/vm/url/template/' + templateId,
        contentType: 'application/json;charset=UTF-8',
        xhrFields: {
            withCredentials: true
        },
        success: function (response) {
            hideLoadingModal();
            var vncUrl = response.url;
            window.location = "/viewer?vncUrl=" + encodeURIComponent(vncUrl);
        },
        error: function (error) {
            alert('Erreur de d\'ouverture de la VM');
            hideLoadingModal(); 
        }
    })
}

function createTemplateCard(template) {
    var templateCard = $('<div>').addClass('card').css('width', '18rem').attr('id', template.id);
    var cardBody = createCardBody(template);
    templateCard.append(cardBody);
    return templateCard;
}

function createCardBody(template) {
    var cardBody = $('<div>').addClass('card-body bg-secondary text-center');
    var icon = $('<i>').addClass('bi bi-pc-display mb-3');
    var img = $('<div>').addClass('text-center').append(icon);
    var form = createForm(template);
    var ldsDefaultContainer = createLdsDefaultContainer(template.id);
    cardBody.append(img, form, ldsDefaultContainer);
    return cardBody;
}

function createForm(template) {
    var form = $('<form>').attr({
        method: 'post',
        id: 'templateForm'
    });
    form.append(
        $('<input>').attr({
            type: 'hidden',
            name: 'template_name',
            value: template.name
        }),
        $('<input>').attr({
            type: 'hidden',
            name: 'template_id',
            value: template.id
        }),
        $('<h5>').addClass('card-title').text(template.name),
        template.description ? $('<p>').addClass('card-text').text(template.description) : null,
        $('<button>').attr({
            id: 'start_vm_btn',
            type: 'button',
            class: 'btn btn-light'
        }).on('click', function () {
            createVmFromTemplate(template.id);
        }).text('Démarrer')
    );
    return form;
}

function createLdsDefaultContainer(templateId) {
    var ldsDefaultContainer = $('<div>').addClass('lds-default-container');
    var ldsDefaultSpinner = createLdsDefaultSpinner(templateId);
    ldsDefaultContainer.append(ldsDefaultSpinner);
    return ldsDefaultContainer;
}

function createLdsDefaultSpinner(templateId) {
    var ldsDefaultSpinner = $('<div>').addClass('lds-default').attr('id', templateId + '-loading-modal');
    for (var i = 0; i < 12; i++) {
        var childDiv = $('<div>');
        ldsDefaultSpinner.append(childDiv);
    }
    return ldsDefaultSpinner;
}

function addTemplateToDOM(template) {
    var templateCard = createTemplateCard(template);
    templatesDiv.append(templateCard);
    getVmStatus(template.id);
}

function getTemplates() {
    $.ajax({
        type: 'GET',
        url: 'https://api.insa-cvl.com/template',
        contentType: 'application/json;charset=UTF-8',
        xhrFields: {
            withCredentials: true
        },
        success: function (response) {
            var templates = response;
            templatesDiv = $('#templates-div');
            templates.forEach(addTemplateToDOM);
        },
        error: function (error) {
            alert('Erreur d\'obtention d\'informations de templates');
        }
    });
}