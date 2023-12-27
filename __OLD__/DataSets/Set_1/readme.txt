Can be found at: https://zenodo.org/record/56198#.ZCH2-i_YnXa

Structure
=========

- im2latex_[...].lst files
    - Each line is separate generated image per formula
    - Line structure: "[formula_idx] [image_name] [render_type]"
        - formula_idx is the line number of the formula in im2latex_formulas.lst
        - image_name is the name of rendered image (without '.png')
        - render_type is the name of used rendering settings (in image2latex.py)
    - Dataset is split to train, validation and test
        - train is for training the model
        - validation is for things testing accuracy while training / checking overfitting
        - test set is for final evaluation 
- im2latex_formulas.lst
    - Each line is a separate formula (formulas were stripped from "\n")
- formula_images.tar.gz (can be found at: https://zenodo.org/record/56198/files/formula_images.tar.gz?download=1)
    - tar file of the rendered images
    - Each image is an image of full "A4" page, where _only_ the formula is rendered
        - -> Lots of empty space
