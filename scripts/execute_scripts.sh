#!/bin/bash

# Fonction pour exécuter extract_corpus.py
function extract_corpus {
    echo "Entrez le chemin du répertoire contenant les fichiers corpus :"
    read corpus_path

    echo "Entrez la date de début (au format YYYY-MM-DD) :"
    read start_date

    echo "Entrez la date de fin (au format YYYY-MM-DD) :"
    read end_date

    echo "Entrez le nom de l'analyseur syntaxique (spacy, trankit, stanza) :"
    read analyzer

    echo "Entrez le format de sortie (xml, json, pickle) :"
    read output_format

    echo "Entrez les catégories à retenir (séparées par un espace) :"
    read categories

    # Exécute du script.py en passant les options en arguments
    python extract_corpus.py -s $start_date -e $end_date -m $analyzer -f $output_format $corpus_path $categories

    # Stockage du chemin et du nom de fichier de sortie dans une variable
    input_file="${start_date}_${end_date}.${output_format}"

    echo "Le fichier de sortie est : $input_file"
}

 # Demande à l'utilisateur s'il souhaite exécuter la fonction extract_corpus
 read -r -p "Voulez-vous exécuter la fonction extract_corpus ? [y/n] : " execute_extract_corpus

if [[ "$execute_extract_corpus" == "y" ]]; then
    # Exécute extract_corpus pour initialiser la variable input_file
    extract_corpus
else
    # Demande le chemin du fichier à traiter à l'utilisateur
    echo "Entrez le chemin du fichier à traiter :"
    read input_file
fi

# Fonction pour exécuter run_lda.py
function run_lda {
    
    # Demande si l'on utilise la forme ou le lemme
    echo "Utiliser la forme (-f) ou le lemme (-l) ?"
    read -r -p "Choisir une option [f/l] : " form_or_lemma
    while [[ "$form_or_lemma" != "f" && "$form_or_lemma" != "l" ]]; do
        echo "Option invalide."
        read -r -p "Choisir une option [f/l] : " form_or_lemma
    done
    
    # Demande les POS à filtrer
    read -r -p "Filtrer sur le POS ? [y/n] : " filter_pos
    if [[ "$filter_pos" == "y" ]]; then
        echo "Liste des POS disponibles : ADJ ADP ADV AUX CONJ DET INTJ NOUN NUM PART PRON PROPN PUNCT SCONJ SYM VERB X"
        read -r -p "Entrez les POS à filtrer (séparés par un espace) : " pos_filter
    else
        pos_filter="ADJ ADP ADV AUX CONJ DET INTJ NOUN NUM PART PRON PROPN PUNCT SCONJ SYM VERB X"
    fi
    
    # Demande le nombre de topics
    read -r -p "Nombre de topics dans le modèle LDA ? (par défaut: 10) : " num_topics
    
    # Demande le fichier de sortie pour la visualisation ldaviz
    read -r -p "Générer la visualisation ldaviz ? [y/n] : " generate_ldaviz
    if [[ "$generate_ldaviz" == "y" ]]; then
        read -r -p "Entrez le chemin et le nom de fichier pour la visualisation ldaviz : " ldaviz_output_file
        ldaviz_option="-o $ldaviz_output_file"
    fi
    
    # Demande l'affichage des topics et de leur cohérence
    read -r -p "Afficher les topics et leur cohérence ? [y/n] : " display_topics_coherence
    if [[ "$display_topics_coherence" == "y" ]]; then
        coherence_option="-c"
    fi
    
    # Demande les valeurs pour no_below et no_above
    read -r -p "Valeur minimale de fréquence d'apparition des mots dans le corpus ? (par défaut: 0.1) : " no_below
    read -r -p "Valeur maximale de fréquence d'apparition des mots dans le corpus ? (par défaut: 0.9) : " no_above
    
    # Exécute le script.py en passant les options en arguments
    if [[ "$form_or_lemma" == "f" ]]; then
        python run_lda.py "$input_file" -f -p $pos_filter -t "${num_topics:-10}" $ldaviz_option $coherence_option --no_below "${no_below:-0.1}" --no_above "${no_above:-0.9}"
    else
        python run_lda.py "$input_file" -l -p $pos_filter -t "${num_topics:-10}" $ldaviz_option $coherence_option --no_below "${no_below:-0.1}" --no_above "${no_above:-0.9}"
    fi
}

# Exécute run_lda
run_lda
