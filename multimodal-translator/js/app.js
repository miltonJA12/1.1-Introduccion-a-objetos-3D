// ==========================================================
// REFERENCIAS GENERALES
// ==========================================================

const modeTabs = document.querySelectorAll(
    '.mode-tab'
);

const modeContents = document.querySelectorAll(
    '.mode-content'
);


// ==========================================================
// CAMBIO DE MODALIDAD
// ==========================================================

modeTabs.forEach((tab) => {

    tab.addEventListener('click', () => {

        const selectedMode =
            tab.dataset.mode;


        // Desactivar botones
        modeTabs.forEach((item) => {

            item.classList.remove(
                'active'
            );

        });


        // Activar botón seleccionado
        tab.classList.add(
            'active'
        );


        // Ocultar módulos
        modeContents.forEach((content) => {

            content.classList.remove(
                'active'
            );

        });


        // Mostrar módulo seleccionado
        const selectedContent =
            document.getElementById(
                `mode-${selectedMode}`
            );


        if (selectedContent) {

            selectedContent.classList.add(
                'active'
            );

        }

    });

});


// ==========================================================
// CONTADOR DE CARACTERES
// ==========================================================

const chatInput =
    document.getElementById(
        'chatInput'
    );

const characterCounter =
    document.getElementById(
        'characterCounter'
    );


chatInput.addEventListener(
    'input',
    () => {

        const currentLength =
            chatInput.value.length;

        characterCounter.textContent =
            `${currentLength} / 2000`;

    }
);


// ==========================================================
// BOTONES PARA SELECCIONAR ARCHIVOS
// ==========================================================

const selectAudio =
    document.getElementById(
        'selectAudio'
    );

const audioFile =
    document.getElementById(
        'audioFile'
    );


selectAudio.addEventListener(
    'click',
    () => {

        audioFile.click();

    }
);


const selectDocument =
    document.getElementById(
        'selectDocument'
    );

const documentFile =
    document.getElementById(
        'documentFile'
    );


selectDocument.addEventListener(
    'click',
    () => {

        documentFile.click();

    }
);


const selectImage =
    document.getElementById(
        'selectImage'
    );

const imageFile =
    document.getElementById(
        'imageFile'
    );


selectImage.addEventListener(
    'click',
    () => {

        imageFile.click();

    }
);


// ==========================================================
// INTERCAMBIAR IDIOMAS
// ==========================================================

const sourceLanguage =
    document.getElementById(
        'sourceLanguage'
    );

const targetLanguage =
    document.getElementById(
        'targetLanguage'
    );

const swapLanguages =
    document.getElementById(
        'swapLanguages'
    );


swapLanguages.addEventListener(
    'click',
    () => {

        const sourceValue =
            sourceLanguage.value;

        const targetValue =
            targetLanguage.value;


        // Si está en automático,
        // utilizamos el idioma contrario al destino.
        if (sourceValue === 'auto') {

            sourceLanguage.value =
                targetValue === 'es'
                    ? 'en'
                    : 'es';

            targetLanguage.value =
                targetValue === 'es'
                    ? 'en'
                    : 'es';

            return;

        }


        sourceLanguage.value =
            targetValue;

        targetLanguage.value =
            sourceValue;

    }
);


// ==========================================================
// NAVEGACIÓN
// ==========================================================

document
    .querySelectorAll(
        'a[href^="#"]'
    )
    .forEach((link) => {

        link.addEventListener(
            'click',
            (event) => {

                const targetId =
                    link.getAttribute(
                        'href'
                    );


                if (
                    !targetId ||
                    targetId === '#'
                ) {

                    return;

                }


                const target =
                    document.querySelector(
                        targetId
                    );


                if (target) {

                    event.preventDefault();

                    target.scrollIntoView({
                        behavior: 'smooth'
                    });

                }

            }
        );

    });