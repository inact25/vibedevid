import re

with open('components/ui/submit-project-form.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

old_step1 = """          {/* STEP 1: BASICS */}
          <div className={currentStep === 1 ? 'block' : 'hidden space-y-6'}>
            <div className="space-y-6">
              <div className="space-y-2">
                <Label
                  htmlFor="title"
                  className="form-label-enhanced"
                >
                  Project Title *
                </Label>
                <Input
                  id="title"
                  name="title"
                  placeholder="Enter your project title"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  className="form-input-enhanced"
                  required
                  disabled={isLoading || isUploading}
                />
              </div>

              <div className="space-y-2">
                <Label
                  htmlFor="tagline"
                  className="form-label-enhanced"
                >
                  Tagline
                </Label>
                <Input
                  id="tagline"
                  name="tagline"
                  placeholder="A short tagline that describes your project in one sentence"
                  value={tagline}
                  onChange={(e) => setTagline(e.target.value)}
                  className="form-input-enhanced"
                  disabled={isLoading || isUploading}
                />
                <p className="form-helper-text mt-1 text-xs">
                  Tagline singkat yang describe project lo dalam satu kalimat! ✨
                </p>
              </div>

              <div className="space-y-2">
                <Label
                  htmlFor="description"
                  className="form-label-enhanced"
                >
                  Description *
                </Label>
                <Textarea
                  id="description"
                  name="description"
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  placeholder="Describe your project, its features, and what makes it special"
                  className="form-input-enhanced"
                  rows={4}
                  required
                  disabled={isLoading || isUploading}
                  maxLength={MAX_DESCRIPTION_LENGTH}
                />
                <div className="flex items-center justify-between text-sm">
                  <p className="form-helper-text mt-1 text-xs">
                    {`Description maksimal ${MAX_DESCRIPTION_LENGTH} karakter untuk konsistensi!`}
                  </p>
                  <span
                    className={`font-medium ${
                      description.length > MAX_DESCRIPTION_LENGTH
                        ? 'text-red-500'
                        : description.length > 1500
                          ? 'text-yellow-500'
                          : 'text-muted-foreground'
                    }`}
                  >
                    {description.length}/{MAX_DESCRIPTION_LENGTH}
                  </span>
                </div>
              </div>

              <div className="space-y-2">
                <Label
                  htmlFor="category"
                  className="form-label-enhanced"
                >
                  Category *
                </Label>
                <Select
                  name="category"
                  required
                  disabled={isLoading || isUploading}
                  value={category}
                  onValueChange={setCategory}
                >
                  <SelectTrigger id="category">
                    <SelectValue placeholder="Select a category" />
                  </SelectTrigger>
                  <SelectContent>
                    {categories.length > 0 ? (
                      categories.map((cat) => (
                        <SelectItem
                          key={cat.id}
                          value={cat.name}
                        >
                          {cat.display_name}
                        </SelectItem>
                      ))
                    ) : (
                      <SelectItem
                        value="no-categories"
                        disabled
                      >
                        No categories available
                      </SelectItem>
                    )}
                  </SelectContent>
                </Select>
              </div>
            </div>
          </div>"""

new_step1 = """          {/* STEP 1: BASICS */}
          <div className={currentStep === 1 ? 'block' : 'hidden space-y-6'}>
            <div className="space-y-6">
              <div className="space-y-2">
                <Label
                  htmlFor="title"
                  className="form-label-enhanced"
                >
                  Project Title *
                </Label>
                <Input
                  id="title"
                  name="title"
                  placeholder="Enter your project title"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  className="form-input-enhanced"
                  required
                  disabled={isLoading || isUploading}
                  maxLength={MAX_TITLE_LENGTH}
                />
                <div className="flex items-center justify-between text-sm">
                  <p className="form-helper-text mt-1 text-xs">
                    Gunakan nama project yang singkat dan jelas.
                  </p>
                  <span
                    className={`font-medium text-xs ${
                      title.length > MAX_TITLE_LENGTH
                        ? 'text-red-500'
                        : title.length > 0 && title.trim().length < MIN_TITLE_LENGTH
                          ? 'text-red-500'
                          : 'text-muted-foreground'
                    }`}
                  >
                    {title.length}/{MAX_TITLE_LENGTH}
                  </span>
                </div>
              </div>

              <div className="space-y-2">
                <Label
                  htmlFor="tagline"
                  className="form-label-enhanced"
                >
                  Tagline
                </Label>
                <Input
                  id="tagline"
                  name="tagline"
                  placeholder="A short tagline that describes your project in one sentence"
                  value={tagline}
                  onChange={(e) => setTagline(e.target.value)}
                  className="form-input-enhanced"
                  disabled={isLoading || isUploading}
                  maxLength={MAX_TAGLINE_LENGTH}
                />
                <div className="flex items-center justify-between text-sm">
                  <p className="form-helper-text mt-1 text-xs">
                    Tagline singkat yang describe project lo dalam satu kalimat! ✨
                  </p>
                  <span
                    className={`font-medium text-xs ${
                      tagline.length > MAX_TAGLINE_LENGTH
                        ? 'text-red-500'
                        : tagline.length > 0 && tagline.trim().length < MIN_TAGLINE_LENGTH
                          ? 'text-amber-500'
                          : 'text-muted-foreground'
                    }`}
                  >
                    {tagline.length}/{MAX_TAGLINE_LENGTH}
                  </span>
                </div>
              </div>

              <div className="space-y-2">
                <Label
                  htmlFor="description"
                  className="form-label-enhanced"
                >
                  Description *
                </Label>
                <Textarea
                  id="description"
                  name="description"
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  placeholder="Describe your project, its feature
