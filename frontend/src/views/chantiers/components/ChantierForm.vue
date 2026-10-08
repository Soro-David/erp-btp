<template>
  <div class="space-y-6">
    <form @submit.prevent="handleSubmit(false)">
      <!-- ===================================================================== -->
      <!-- SECTION 1 — INFORMATIONS GÉNÉRALES -->
      <!-- ===================================================================== -->
      <div class="bg-white border border-slate-200 rounded-2xl p-5 sm:p-7 shadow-sm mb-6 space-y-5">
        <div class="flex items-center justify-between pb-3 border-b border-slate-100">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-xl bg-blue-50 text-[#1d4ed8] flex items-center justify-center text-lg font-bold">
              <fas-icon icon="circle-info" />
            </div>
            <div>
              <h2 class="text-base sm:text-lg font-bold text-slate-900">1. Informations générales</h2>
              <p class="text-xs text-slate-500">Identification, nomenclature et catégorisation de l'ouvrage</p>
            </div>
          </div>
          <span class="px-2.5 py-1 rounded-full text-xs font-semibold bg-blue-50 text-blue-700 border border-blue-200">
            Étape 1/10
          </span>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <!-- Code Chantier (Génération automatique, non modifiable) -->
          <div>
            <label class="block text-xs font-bold text-slate-700 mb-1">
              Code chantier <span class="text-slate-400 font-normal">(Auto-généré)</span>
            </label>
            <div class="relative flex items-center">
              <input
                v-model="form.code"
                type="text"
                readonly
                disabled
                class="w-full pl-3.5 pr-10 py-2.5 rounded-xl bg-slate-100 border border-slate-200 text-slate-700 font-mono font-bold text-sm cursor-not-allowed select-none"
              />
              <button
                type="button"
                @click="fetchNextCode"
                title="Actualiser le code"
                class="absolute right-2 text-slate-400 hover:text-blue-600 p-1.5 transition-colors"
              >
                <fas-icon icon="arrows-rotate" class="text-xs" :class="{ 'animate-spin': loadingCode }" />
              </button>
            </div>
            <p class="text-[11px] text-slate-400 mt-1">Format séquentiel normalisé BTP</p>
          </div>

          <!-- Nom du chantier * -->
          <div class="md:col-span-2">
            <label class="block text-xs font-bold text-slate-700 mb-1">
              Nom du chantier <span class="text-rose-500">*</span>
            </label>
            <input
              v-model="form.name"
              type="text"
              required
              placeholder="Ex: Construction Immeuble Le Récif R+5"
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 text-sm focus:outline-none focus:bg-white focus:border-blue-600 focus:ring-2 focus:ring-blue-100 transition-all"
              :class="{ 'border-rose-400': errors.name }"
            />
            <p v-if="errors.name" class="text-[11px] text-rose-500 mt-1">{{ errors.name }}</p>
          </div>

          <!-- Statut initial * -->
          <div>
            <label class="block text-xs font-bold text-slate-700 mb-1">
              Statut initial <span class="text-rose-500">*</span>
            </label>
            <div class="relative">
              <select
                v-model="form.status"
                required
                class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 text-sm focus:outline-none focus:bg-white focus:border-blue-600 focus:ring-2 focus:ring-blue-100 appearance-none pr-9 cursor-pointer"
              >
                <option value="En préparation">En préparation</option>
                <option value="En cours">En cours</option>
                <option value="Suspendu">Suspendu</option>
                <option value="Terminé">Terminé</option>
              </select>
              <fas-icon icon="chevron-down" class="text-slate-400 absolute right-3.5 top-1/2 -translate-y-1/2 pointer-events-none text-xs" />
            </div>
          </div>
        </div>

        <!-- Type de chantier avec bouton [+] d'ajout dynamique -->
        <div>
          <label class="block text-xs font-bold text-slate-700 mb-1">
            Type de chantier <span class="text-rose-500">*</span>
          </label>
          <div class="flex items-center gap-2">
            <div class="relative flex-1">
              <select
                v-model="form.type_id"
                required
                @change="handleTypeChange"
                class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 text-sm focus:outline-none focus:bg-white focus:border-blue-600 focus:ring-2 focus:ring-blue-100 appearance-none pr-9 cursor-pointer"
                :class="{ 'border-rose-400': errors.type_id }"
              >
                <option :value="null" disabled>Sélectionner un type de chantier...</option>
                <option v-for="t in chantierTypes" :key="t.id" :value="t.id">
                  {{ t.name }}
                </option>
              </select>
              <fas-icon icon="chevron-down" class="text-slate-400 absolute right-3.5 top-1/2 -translate-y-1/2 pointer-events-none text-xs" />
            </div>
            <!-- Bouton [+] pour ouvrir la modal d'ajout de type -->
            <button
              type="button"
              @click="showAddTypeModal = true"
              class="h-10 px-3 rounded-xl bg-blue-50 border border-blue-200 text-[#1d4ed8] hover:bg-blue-600 hover:text-white font-bold text-xs transition-colors flex items-center gap-1.5 shadow-sm"
              title="Ajouter un nouveau type de chantier"
            >
              <fas-icon icon="plus" />
              <span class="hidden sm:inline">Nouveau type</span>
            </button>
          </div>
          <p v-if="errors.type_id" class="text-[11px] text-rose-500 mt-1">{{ errors.type_id }}</p>
        </div>

        <!-- Description du chantier -->
        <div>
          <label class="block text-xs font-semibold text-slate-700 mb-1">
            Description synthétique du projet
          </label>
          <textarea
            v-model="form.description"
            rows="2"
            placeholder="Objectifs, contexte, consistance générale des travaux..."
            class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 text-sm focus:outline-none focus:bg-white focus:border-blue-600 focus:ring-2 focus:ring-blue-100 transition-all resize-none"
          ></textarea>
        </div>
      </div>

      <!-- ===================================================================== -->
      <!-- SECTION 2 — LOCALISATION DU CHANTIER -->
      <!-- ===================================================================== -->
      <div class="bg-white border border-slate-200 rounded-2xl p-5 sm:p-7 shadow-sm mb-6 space-y-5">
        <div class="flex items-center justify-between pb-3 border-b border-slate-100">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-xl bg-emerald-50 text-[#047857] flex items-center justify-center text-lg font-bold">
              <fas-icon icon="location-dot" />
            </div>
            <div>
              <h2 class="text-base sm:text-lg font-bold text-slate-900">2. Localisation du chantier</h2>
              <p class="text-xs text-slate-500">Adresse géographique, ville et coordonnées GPS</p>
            </div>
          </div>
          <!-- Bouton Localiser GPS -->
          <button
            type="button"
            @click="locateGps"
            :disabled="locatingGps"
            class="px-3 py-1.5 rounded-xl bg-emerald-50 hover:bg-emerald-100 border border-emerald-200 text-emerald-800 text-xs font-bold transition-all flex items-center gap-1.5 shadow-sm"
          >
            <fas-icon icon="crosshairs" :class="{ 'animate-spin': locatingGps }" />
            <span>{{ locatingGps ? 'Localisation...' : '📍 Localiser (GPS)' }}</span>
          </button>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <!-- Pays * -->
          <div>
            <label class="block text-xs font-bold text-slate-700 mb-1">
              Pays <span class="text-rose-500">*</span>
            </label>
            <input
              v-model="form.country"
              type="text"
              required
              placeholder="Ex: Côte d'Ivoire"
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 text-sm focus:outline-none focus:bg-white focus:border-blue-600 focus:ring-2 focus:ring-blue-100 transition-all"
            />
          </div>

          <!-- Ville * -->
          <div>
            <label class="block text-xs font-bold text-slate-700 mb-1">
              Ville <span class="text-rose-500">*</span>
            </label>
            <input
              v-model="form.city"
              type="text"
              required
              placeholder="Ex: Abidjan, Yamoussoukro..."
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 text-sm focus:outline-none focus:bg-white focus:border-blue-600 focus:ring-2 focus:ring-blue-100 transition-all"
              :class="{ 'border-rose-400': errors.city }"
            />
            <p v-if="errors.city" class="text-[11px] text-rose-500 mt-1">{{ errors.city }}</p>
          </div>

          <!-- Commune -->
          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1">
              Commune
            </label>
            <input
              v-model="form.commune"
              type="text"
              placeholder="Ex: Cocody, Yopougon, Plateau..."
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 text-sm focus:outline-none focus:bg-white focus:border-blue-600 focus:ring-2 focus:ring-blue-100 transition-all"
            />
          </div>

          <!-- Quartier -->
          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1">
              Quartier / Zone
            </label>
            <input
              v-model="form.district"
              type="text"
              placeholder="Ex: Riviera Golf, Zone Industrielle..."
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 text-sm focus:outline-none focus:bg-white focus:border-blue-600 focus:ring-2 focus:ring-blue-100 transition-all"
            />
          </div>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <!-- Adresse précise -->
          <div class="sm:col-span-2">
            <label class="block text-xs font-semibold text-slate-700 mb-1">
              Adresse précise / Repères d'accès
            </label>
            <input
              v-model="form.address"
              type="text"
              placeholder="Ex: Boulevard de France, face station Shell..."
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 text-sm focus:outline-none focus:bg-white focus:border-blue-600 focus:ring-2 focus:ring-blue-100 transition-all"
            />
          </div>

          <!-- Coordonnées GPS (Latitude / Longitude) -->
          <div class="grid grid-cols-2 gap-2">
            <div>
              <label class="block text-[11px] font-semibold text-slate-600 mb-1">Latitude</label>
              <input
                v-model.number="form.latitude"
                type="number"
                step="any"
                placeholder="5.3599"
                class="w-full px-2.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 text-xs font-mono focus:outline-none focus:bg-white focus:border-blue-600"
              />
            </div>
            <div>
              <label class="block text-[11px] font-semibold text-slate-600 mb-1">Longitude</label>
              <input
                v-model.number="form.longitude"
                type="number"
                step="any"
                placeholder="-4.0083"
                class="w-full px-2.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 text-xs font-mono focus:outline-none focus:bg-white focus:border-blue-600"
              />
            </div>
          </div>
        </div>
      </div>

      <!-- ===================================================================== -->
      <!-- SECTION 3 — INFORMATIONS CLIENT & MAÎTRE D'OUVRAGE -->
      <!-- ===================================================================== -->
      <div class="bg-white border border-slate-200 rounded-2xl p-5 sm:p-7 shadow-sm mb-6 space-y-5">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-100">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-xl bg-amber-50 text-amber-600 flex items-center justify-center text-lg font-bold">
              <fas-icon icon="user-tie" />
            </div>
            <div>
              <h2 class="text-base sm:text-lg font-bold text-slate-900">3. Informations client / Maître d'ouvrage</h2>
              <p class="text-xs text-slate-500">Sélection d'un client existant ou création à la volée</p>
            </div>
          </div>

          <!-- Bascule Client existant / Nouveau client -->
          <div class="inline-flex p-1 bg-slate-100 rounded-xl border border-slate-200 self-start sm:self-auto">
            <button
              type="button"
              @click="clientMode = 'existing'"
              class="px-3 py-1.5 rounded-lg text-xs font-bold transition-all"
              :class="clientMode === 'existing' ? 'bg-white text-blue-700 shadow-sm' : 'text-slate-600 hover:text-slate-900'"
            >
              Client existant
            </button>
            <button
              type="button"
              @click="clientMode = 'new'"
              class="px-3 py-1.5 rounded-lg text-xs font-bold transition-all"
              :class="clientMode === 'new' ? 'bg-white text-blue-700 shadow-sm' : 'text-slate-600 hover:text-slate-900'"
            >
              + Nouveau client
            </button>
          </div>
        </div>

        <!-- 3.A. Mode Client Existant -->
        <div v-if="clientMode === 'existing'" class="space-y-4">
          <div>
            <label class="block text-xs font-bold text-slate-700 mb-1">
              Sélectionner un client dans la liste <span class="text-rose-500">*</span>
            </label>
            <div class="relative">
              <select
                v-model="form.client_id"
                @change="handleClientSelect"
                class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 text-sm focus:outline-none focus:bg-white focus:border-blue-600 appearance-none pr-9 cursor-pointer"
                :class="{ 'border-rose-400': errors.client_id }"
              >
                <option :value="null" disabled>Choisir un client enregistré...</option>
                <option v-for="c in clientsList" :key="c.id" :value="c.id">
                  {{ c.name }} ({{ c.type }})
                </option>
              </select>
              <fas-icon icon="chevron-down" class="text-slate-400 absolute right-3.5 top-1/2 -translate-y-1/2 pointer-events-none text-xs" />
            </div>
            <p v-if="errors.client_id" class="text-[11px] text-rose-500 mt-1">{{ errors.client_id }}</p>
          </div>

          <!-- Aperçu du client sélectionné -->
          <div v-if="selectedClientSummary" class="p-3.5 rounded-xl bg-slate-50 border border-slate-200 text-xs flex flex-wrap gap-4 text-slate-600">
            <div><strong>Type :</strong> {{ selectedClientSummary.type }}</div>
            <div v-if="selectedClientSummary.phone"><strong>Tél :</strong> {{ selectedClientSummary.phone }}</div>
            <div v-if="selectedClientSummary.email"><strong>Email :</strong> {{ selectedClientSummary.email }}</div>
            <div v-if="selectedClientSummary.contact_person"><strong>Contact :</strong> {{ selectedClientSummary.contact_person }}</div>
          </div>
        </div>

        <!-- 3.B. Mode Nouveau Client -->
        <div v-else class="space-y-4">
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <!-- Type de client * -->
            <div>
              <label class="block text-xs font-bold text-slate-700 mb-1">
                Type de client <span class="text-rose-500">*</span>
              </label>
              <div class="relative">
                <select
                  v-model="newClient.type"
                  class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 text-sm focus:outline-none focus:bg-white focus:border-blue-600 appearance-none pr-9 cursor-pointer"
                >
                  <option value="Particulier">Particulier</option>
                  <option value="Entreprise">Entreprise</option>
                  <option value="Administration publique">Administration publique</option>
                </select>
                <fas-icon icon="chevron-down" class="text-slate-400 absolute right-3.5 top-1/2 -translate-y-1/2 pointer-events-none text-xs" />
              </div>
            </div>

            <!-- Nom / Raison sociale * -->
            <div class="sm:col-span-2">
              <label class="block text-xs font-bold text-slate-700 mb-1">
                Nom ou Raison sociale <span class="text-rose-500">*</span>
              </label>
              <input
                v-model="newClient.name"
                type="text"
                placeholder="Ex: Ministère de l'Équipement, SCI Laguna, M. Jean Touré..."
                class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 text-sm focus:outline-none focus:bg-white focus:border-blue-600"
                :class="{ 'border-rose-400': errors.client_name }"
              />
              <p v-if="errors.client_name" class="text-[11px] text-rose-500 mt-1">{{ errors.client_name }}</p>
            </div>
          </div>

          <!-- Contacts généraux -->
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div>
              <label class="block text-xs font-semibold text-slate-700 mb-1">Téléphone</label>
              <input
                v-model="newClient.phone"
                type="tel"
                placeholder="+225 27 00 00 00"
                class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 text-sm focus:outline-none focus:bg-white focus:border-blue-600"
              />
            </div>
            <div>
              <label class="block text-xs font-semibold text-slate-700 mb-1">Email</label>
              <input
                v-model="newClient.email"
                type="email"
                placeholder="client@domaine.ci"
                class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 text-sm focus:outline-none focus:bg-white focus:border-blue-600"
              />
            </div>
            <div>
              <label class="block text-xs font-semibold text-slate-700 mb-1">Personne à contacter</label>
              <input
                v-model="newClient.contact_person"
                type="text"
                placeholder="Ex: M. Coulibaly, Dir. Technique"
                class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 text-sm focus:outline-none focus:bg-white focus:border-blue-600"
              />
            </div>
          </div>

          <!-- CHAMPS CONDITIONNELS : ENTREPRISE -->
          <div
            v-if="newClient.type === 'Entreprise'"
            class="p-4 rounded-xl bg-blue-50/50 border border-blue-200/70 space-y-3"
          >
            <div class="flex items-center gap-2 text-xs font-bold text-blue-800 uppercase tracking-wider">
              <fas-icon icon="building" />
              <span>Détails légaux Entreprise</span>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
              <div>
                <label class="block text-[11px] font-semibold text-slate-700 mb-1">Raison sociale</label>
                <input
                  v-model="newClient.company_name"
                  type="text"
                  placeholder="Ex: SOGEPRIM SARL"
                  class="w-full px-3 py-2 rounded-lg bg-white border border-slate-200 text-xs text-slate-900"
                />
              </div>
              <div>
                <label class="block text-[11px] font-semibold text-slate-700 mb-1">N° RCCM</label>
                <input
                  v-model="newClient.rccm"
                  type="text"
                  placeholder="Ex: CI-ABJ-2024-B-0145"
                  class="w-full px-3 py-2 rounded-lg bg-white border border-slate-200 text-xs text-slate-900 font-mono"
                />
              </div>
              <div>
                <label class="block text-[11px] font-semibold text-slate-700 mb-1">Contact entreprise (Ligne directe)</label>
                <input
                  v-model="newClient.company_contact"
                  type="text"
                  placeholder="Ex: +225 07 10 20 30"
                  class="w-full px-3 py-2 rounded-lg bg-white border border-slate-200 text-xs text-slate-900"
                />
              </div>
            </div>
          </div>

          <!-- CHAMPS CONDITIONNELS : ADMINISTRATION PUBLIQUE -->
          <div
            v-if="newClient.type === 'Administration publique'"
            class="p-4 rounded-xl bg-emerald-50/50 border border-emerald-200/70 space-y-3"
          >
            <div class="flex items-center gap-2 text-xs font-bold text-emerald-800 uppercase tracking-wider">
              <fas-icon icon="landmark" />
              <span>Rattachement Administratif</span>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-4 gap-3">
              <div>
                <label class="block text-[11px] font-semibold text-slate-700 mb-1">Ministère / Institution</label>
                <input
                  v-model="newClient.ministry"
                  type="text"
                  placeholder="Ex: Ministère de l'Éducation"
                  class="w-full px-3 py-2 rounded-lg bg-white border border-slate-200 text-xs text-slate-900"
                />
              </div>
              <div>
                <label class="block text-[11px] font-semibold text-slate-700 mb-1">Direction</label>
                <input
                  v-model="newClient.direction"
                  type="text"
                  placeholder="Ex: DAF / Dir. Patrimoine"
                  class="w-full px-3 py-2 rounded-lg bg-white border border-slate-200 text-xs text-slate-900"
                />
              </div>
              <div>
                <label class="block text-[11px] font-semibold text-slate-700 mb-1">Service</label>
                <input
                  v-model="newClient.service"
                  type="text"
                  placeholder="Ex: Service Marchés Publics"
                  class="w-full px-3 py-2 rounded-lg bg-white border border-slate-200 text-xs text-slate-900"
                />
              </div>
              <div>
                <label class="block text-[11px] font-semibold text-slate-700 mb-1">Responsable administratif</label>
                <input
                  v-model="newClient.admin_in_charge"
                  type="text"
                  placeholder="Ex: M. Koffi K."
                  class="w-full px-3 py-2 rounded-lg bg-white border border-slate-200 text-xs text-slate-900"
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ===================================================================== -->
      <!-- SECTION 4 — RESPONSABLES DU CHANTIER -->
      <!-- ===================================================================== -->
      <div class="bg-white border border-slate-200 rounded-2xl p-5 sm:p-7 shadow-sm mb-6 space-y-5">
        <div class="flex items-center justify-between pb-3 border-b border-slate-100">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-xl bg-purple-50 text-purple-700 flex items-center justify-center text-lg font-bold">
              <fas-icon icon="users-gear" />
            </div>
            <div>
              <h2 class="text-base sm:text-lg font-bold text-slate-900">4. Responsables & Intervenants clés</h2>
              <p class="text-xs text-slate-500">Affectation des rôles opérationnels avec bouton d'ajout rapide [+]</p>
            </div>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          <!-- Chef de projet -->
          <div>
            <label class="block text-xs font-bold text-slate-700 mb-1">
              Chef de projet
            </label>
            <div class="flex items-center gap-2">
              <div class="relative flex-1">
                <select
                  v-model="form.project_manager_id"
                  class="w-full px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 text-xs focus:outline-none focus:bg-white focus:border-blue-600 appearance-none pr-8 cursor-pointer"
                >
                  <option :value="null">Non assigné</option>
                  <option v-for="r in filteredResponsables('Chef de projet')" :key="r.id" :value="r.id">
                    {{ r.full_name }}
                  </option>
                </select>
                <fas-icon icon="chevron-down" class="text-slate-400 absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none text-[10px]" />
              </div>
              <button
                type="button"
                @click="openAddResponsableModal('Chef de projet', 'project_manager_id')"
                class="w-9 h-9 rounded-xl bg-purple-50 text-purple-700 hover:bg-purple-600 hover:text-white border border-purple-200 flex items-center justify-center text-xs transition-colors shadow-sm flex-shrink-0"
                title="Ajouter un Chef de projet"
              >
                <fas-icon icon="plus" />
              </button>
            </div>
          </div>

          <!-- Conducteur des travaux -->
          <div>
            <label class="block text-xs font-bold text-slate-700 mb-1">
              Conducteur des travaux
            </label>
            <div class="flex items-center gap-2">
              <div class="relative flex-1">
                <select
                  v-model="form.site_manager_id"
                  class="w-full px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 text-xs focus:outline-none focus:bg-white focus:border-blue-600 appearance-none pr-8 cursor-pointer"
                >
                  <option :value="null">Non assigné</option>
                  <option v-for="r in filteredResponsables('Conducteur des travaux')" :key="r.id" :value="r.id">
                    {{ r.full_name }}
                  </option>
                </select>
                <fas-icon icon="chevron-down" class="text-slate-400 absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none text-[10px]" />
              </div>
              <button
                type="button"
                @click="openAddResponsableModal('Conducteur des travaux', 'site_manager_id')"
                class="w-9 h-9 rounded-xl bg-purple-50 text-purple-700 hover:bg-purple-600 hover:text-white border border-purple-200 flex items-center justify-center text-xs transition-colors shadow-sm flex-shrink-0"
                title="Ajouter un Conducteur des travaux"
              >
                <fas-icon icon="plus" />
              </button>
            </div>
          </div>

          <!-- Chef de chantier -->
          <div>
            <label class="block text-xs font-bold text-slate-700 mb-1">
              Chef de chantier
            </label>
            <div class="flex items-center gap-2">
              <div class="relative flex-1">
                <select
                  v-model="form.foreman_id"
                  class="w-full px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 text-xs focus:outline-none focus:bg-white focus:border-blue-600 appearance-none pr-8 cursor-pointer"
                >
                  <option :value="null">Non assigné</option>
                  <option v-for="r in filteredResponsables('Chef de chantier')" :key="r.id" :value="r.id">
                    {{ r.full_name }}
                  </option>
                </select>
                <fas-icon icon="chevron-down" class="text-slate-400 absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none text-[10px]" />
              </div>
              <button
                type="button"
                @click="openAddResponsableModal('Chef de chantier', 'foreman_id')"
                class="w-9 h-9 rounded-xl bg-purple-50 text-purple-700 hover:bg-purple-600 hover:text-white border border-purple-200 flex items-center justify-center text-xs transition-colors shadow-sm flex-shrink-0"
                title="Ajouter un Chef de chantier"
              >
                <fas-icon icon="plus" />
              </button>
            </div>
          </div>

          <!-- Responsable HSE -->
          <div>
            <label class="block text-xs font-bold text-slate-700 mb-1">
              Responsable HSE (Hygiène Sécurité Environnement)
            </label>
            <div class="flex items-center gap-2">
              <div class="relative flex-1">
                <select
                  v-model="form.hse_officer_id"
                  class="w-full px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 text-xs focus:outline-none focus:bg-white focus:border-blue-600 appearance-none pr-8 cursor-pointer"
                >
                  <option :value="null">Non assigné</option>
                  <option v-for="r in filteredResponsables('Responsable HSE')" :key="r.id" :value="r.id">
                    {{ r.full_name }}
                  </option>
                </select>
                <fas-icon icon="chevron-down" class="text-slate-400 absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none text-[10px]" />
              </div>
              <button
                type="button"
                @click="openAddResponsableModal('Responsable HSE', 'hse_officer_id')"
                class="w-9 h-9 rounded-xl bg-purple-50 text-purple-700 hover:bg-purple-600 hover:text-white border border-purple-200 flex items-center justify-center text-xs transition-colors shadow-sm flex-shrink-0"
                title="Ajouter un Responsable HSE"
              >
                <fas-icon icon="plus" />
              </button>
            </div>
          </div>

          <!-- Bureau d'études -->
          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1">
              Bureau d'études technique
            </label>
            <input
              v-model="form.design_office"
              type="text"
              placeholder="Ex: Cabinet Structure CI, Veritas..."
              class="w-full px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 text-xs focus:outline-none focus:bg-white focus:border-blue-600"
            />
          </div>

          <!-- Entreprise exécutante -->
          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1">
              Entreprise exécutante / Sous-traitant principal
            </label>
            <input
              v-model="form.contractor"
              type="text"
              placeholder="Ex: SIT BTP, EBOMAF, Régie interne..."
              class="w-full px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 text-xs focus:outline-none focus:bg-white focus:border-blue-600"
            />
          </div>
        </div>
      </div>

      <!-- ===================================================================== -->
      <!-- SECTION 5 — PLANNING & CALENDRIER -->
      <!-- ===================================================================== -->
      <div class="bg-white border border-slate-200 rounded-2xl p-5 sm:p-7 shadow-sm mb-6 space-y-5">
        <div class="flex items-center justify-between pb-3 border-b border-slate-100">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center text-lg font-bold">
              <fas-icon icon="calendar-days" />
            </div>
            <div>
              <h2 class="text-base sm:text-lg font-bold text-slate-900">5. Planning & Délais</h2>
              <p class="text-xs text-slate-500">Dates contractuelles et calcul dynamique de la durée</p>
            </div>
          </div>

          <!-- Durée calculée automatiquement avec badge dynamique -->
          <div class="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-blue-50 border border-blue-200 text-[#1d4ed8]">
            <fas-icon icon="stopwatch" class="text-xs" />
            <span class="text-xs font-black">
              Durée estimée : {{ calculatedDurationText }}
            </span>
          </div>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <!-- Date de début prévue * -->
          <div>
            <label class="block text-xs font-bold text-slate-700 mb-1">
              Date début prévue <span class="text-rose-500">*</span>
            </label>
            <input
              v-model="form.start_date_planned"
              type="date"
              required
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 text-sm focus:outline-none focus:bg-white focus:border-blue-600"
              :class="{ 'border-rose-400': errors.start_date_planned }"
            />
            <p v-if="errors.start_date_planned" class="text-[11px] text-rose-500 mt-1">{{ errors.start_date_planned }}</p>
          </div>

          <!-- Date de fin prévue * -->
          <div>
            <label class="block text-xs font-bold text-slate-700 mb-1">
              Date fin prévue <span class="text-rose-500">*</span>
            </label>
            <input
              v-model="form.end_date_planned"
              type="date"
              required
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 text-sm focus:outline-none focus:bg-white focus:border-blue-600"
              :class="{ 'border-rose-400': errors.end_date_planned }"
            />
            <p v-if="errors.end_date_planned" class="text-[11px] text-rose-500 mt-1">{{ errors.end_date_planned }}</p>
          </div>

          <!-- Date réelle début (optionnelle) -->
          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1">
              Date réelle de début <span class="text-slate-400 font-normal">(si démarré)</span>
            </label>
            <input
              v-model="form.start_date_actual"
              type="date"
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 text-sm focus:outline-none focus:bg-white focus:border-blue-600"
            />
          </div>

          <!-- Date réelle fin (optionnelle) -->
          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1">
              Date réelle de fin <span class="text-slate-400 font-normal">(réception)</span>
            </label>
            <input
              v-model="form.end_date_actual"
              type="date"
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 text-sm focus:outline-none focus:bg-white focus:border-blue-600"
            />
          </div>
        </div>
      </div>

      <!-- ===================================================================== -->
      <!-- SECTION 6 — INFORMATIONS FINANCIÈRES -->
      <!-- ===================================================================== -->
      <div class="bg-white border border-slate-200 rounded-2xl p-5 sm:p-7 shadow-sm mb-6 space-y-5">
        <div class="flex items-center justify-between pb-3 border-b border-slate-100">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-xl bg-emerald-50 text-emerald-700 flex items-center justify-center text-lg font-bold">
              <fas-icon icon="money-bill-wave" />
            </div>
            <div>
              <h2 class="text-base sm:text-lg font-bold text-slate-900">6. Informations financières & Marché</h2>
              <p class="text-xs text-slate-500">Budgets prévisionnels, enveloppe marché et mode de financement</p>
            </div>
          </div>
          <span class="text-xs font-bold text-slate-500 uppercase tracking-wider">Devise : {{ form.currency }}</span>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
          <!-- Devise * -->
          <div>
            <label class="block text-xs font-bold text-slate-700 mb-1">
              Devise <span class="text-rose-500">*</span>
            </label>
            <div class="relative">
              <select
                v-model="form.currency"
                required
                class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 text-sm font-bold focus:outline-none focus:bg-white focus:border-blue-600 appearance-none pr-9 cursor-pointer"
              >
                <option value="FCFA">FCFA (XOF)</option>
                <option value="EUR">Euro (€)</option>
                <option value="USD">Dollar ($)</option>
              </select>
              <fas-icon icon="chevron-down" class="text-slate-400 absolute right-3.5 top-1/2 -translate-y-1/2 pointer-events-none text-xs" />
            </div>
          </div>

          <!-- Montant du marché -->
          <div>
            <label class="block text-xs font-bold text-slate-700 mb-1">
              Montant du marché
            </label>
            <input
              v-model.number="form.contract_amount"
              type="number"
              min="0"
              placeholder="0"
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 font-mono text-sm focus:outline-none focus:bg-white focus:border-blue-600"
            />
            <p class="text-[10px] text-slate-400 mt-1 font-mono">{{ formatCurrencyDisplay(form.contract_amount) }}</p>
          </div>

          <!-- Budget prévisionnel -->
          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1">
              Budget prévisionnel
            </label>
            <input
              v-model.number="form.budget_estimated"
              type="number"
              min="0"
              placeholder="0"
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 font-mono text-sm focus:outline-none focus:bg-white focus:border-blue-600"
            />
            <p class="text-[10px] text-slate-400 mt-1 font-mono">{{ formatCurrencyDisplay(form.budget_estimated) }}</p>
          </div>

          <!-- Coût estimatif travaux -->
          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1">
              Coût estimatif interne
            </label>
            <input
              v-model.number="form.cost_estimated"
              type="number"
              min="0"
              placeholder="0"
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 font-mono text-sm focus:outline-none focus:bg-white focus:border-blue-600"
            />
            <p class="text-[10px] text-slate-400 mt-1 font-mono">{{ formatCurrencyDisplay(form.cost_estimated) }}</p>
          </div>

          <!-- Mode de financement -->
          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1">
              Mode de financement
            </label>
            <div class="relative">
              <select
                v-model="form.funding_mode"
                class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 text-xs focus:outline-none focus:bg-white focus:border-blue-600 appearance-none pr-8 cursor-pointer"
              >
                <option value="Fonds propres">Fonds propres</option>
                <option value="Crédit bancaire">Crédit bancaire</option>
                <option value="État / Marché Public">État / Marché Public</option>
                <option value="Bailleur international">Bailleur international</option>
                <option value="Partenariat Public-Privé">Partenariat Public-Privé (PPP)</option>
                <option value="Autre">Autre</option>
              </select>
              <fas-icon icon="chevron-down" class="text-slate-400 absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none text-[10px]" />
            </div>
          </div>
        </div>
      </div>

      <!-- ===================================================================== -->
      <!-- SECTION 7 — INFORMATIONS TECHNIQUES -->
      <!-- ===================================================================== -->
      <div class="bg-white border border-slate-200 rounded-2xl p-5 sm:p-7 shadow-sm mb-6 space-y-5">
        <div class="flex items-center justify-between pb-3 border-b border-slate-100">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-xl bg-indigo-50 text-indigo-700 flex items-center justify-center text-lg font-bold">
              <fas-icon icon="ruler-combined" />
            </div>
            <div>
              <h2 class="text-base sm:text-lg font-bold text-slate-900">7. Spécifications techniques de l'ouvrage</h2>
              <p class="text-xs text-slate-500">Dimensions, hauteur, nature du sol et procédés constructifs</p>
            </div>
          </div>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          <!-- Surface totale en m² -->
          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1">Surface totale (m²)</label>
            <input
              v-model.number="form.surface_m2"
              type="number"
              min="0"
              step="0.01"
              placeholder="Ex: 2450.5"
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 text-sm focus:outline-none focus:bg-white focus:border-blue-600"
            />
          </div>

          <!-- Nombre de bâtiments -->
          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1">Nombre de bâtiments / blocs</label>
            <input
              v-model.number="form.buildings_count"
              type="number"
              min="1"
              placeholder="Ex: 2"
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 text-sm focus:outline-none focus:bg-white focus:border-blue-600"
            />
          </div>

          <!-- Nombre d'étages -->
          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1">Nombre d'étages (R+...)</label>
            <input
              v-model.number="form.floors_count"
              type="number"
              min="0"
              placeholder="Ex: 5 (pour R+5)"
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 text-sm focus:outline-none focus:bg-white focus:border-blue-600"
            />
          </div>

          <!-- Nature du sol -->
          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1">Nature du sol</label>
            <input
              v-model="form.soil_nature"
              type="text"
              placeholder="Ex: Argileux, Sablonneux, Rocheux..."
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 text-sm focus:outline-none focus:bg-white focus:border-blue-600"
            />
          </div>

          <!-- Méthode de construction -->
          <div class="lg:col-span-2">
            <label class="block text-xs font-semibold text-slate-700 mb-1">Méthode de construction</label>
            <input
              v-model="form.construction_method"
              type="text"
              placeholder="Ex: Béton armé coulé sur place, Charpente métallique, Préfabriqué..."
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 text-sm focus:outline-none focus:bg-white focus:border-blue-600"
            />
          </div>
        </div>

        <!-- Description technique détaillée -->
        <div>
          <label class="block text-xs font-semibold text-slate-700 mb-1">Description technique complémentaire</label>
          <textarea
            v-model="form.technical_description"
            rows="2"
            placeholder="Notes sur les fondations, réseaux VRD, contraintes d'accès ou d'approvisionnement..."
            class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 text-sm focus:outline-none focus:bg-white focus:border-blue-600 resize-none"
          ></textarea>
        </div>
      </div>

      <!-- ===================================================================== -->
      <!-- SECTION 8 — SUIVI INITIAL & PRIORITÉ -->
      <!-- ===================================================================== -->
      <div class="bg-white border border-slate-200 rounded-2xl p-5 sm:p-7 shadow-sm mb-6 space-y-5">
        <div class="flex items-center justify-between pb-3 border-b border-slate-100">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-xl bg-teal-50 text-teal-700 flex items-center justify-center text-lg font-bold">
              <fas-icon icon="chart-pie" />
            </div>
            <div>
              <h2 class="text-base sm:text-lg font-bold text-slate-900">8. Suivi initial & Priorité opérationnelle</h2>
              <p class="text-xs text-slate-500">Indicateurs de départ initialisés à 0 %</p>
            </div>
          </div>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-3 gap-5">
          <!-- Avancement physique (%) -->
          <div class="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-2">
            <div class="flex items-center justify-between">
              <span class="text-xs font-bold text-slate-700">Avancement physique</span>
              <span class="text-xs font-black text-blue-700">{{ form.physical_progress }} %</span>
            </div>
            <div class="w-full bg-slate-200 h-2 rounded-full overflow-hidden">
              <div class="bg-blue-600 h-full rounded-full transition-all" :style="{ width: `${form.physical_progress}%` }"></div>
            </div>
            <p class="text-[11px] text-slate-400">Verrouillé à 0 % à la création</p>
          </div>

          <!-- Avancement financier (%) -->
          <div class="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-2">
            <div class="flex items-center justify-between">
              <span class="text-xs font-bold text-slate-700">Avancement financier</span>
              <span class="text-xs font-black text-emerald-700">{{ form.financial_progress }} %</span>
            </div>
            <div class="w-full bg-slate-200 h-2 rounded-full overflow-hidden">
              <div class="bg-emerald-600 h-full rounded-full transition-all" :style="{ width: `${form.financial_progress}%` }"></div>
            </div>
            <p class="text-[11px] text-slate-400">Calculé au fur et à mesure des situations</p>
          </div>

          <!-- Priorité opérationnelle -->
          <div>
            <label class="block text-xs font-bold text-slate-700 mb-1">
              Priorité stratégique <span class="text-rose-500">*</span>
            </label>
            <div class="relative">
              <select
                v-model="form.priority"
                required
                class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 text-sm font-semibold focus:outline-none focus:bg-white focus:border-blue-600 appearance-none pr-9 cursor-pointer"
              >
                <option value="Faible">🟢 Faible</option>
                <option value="Normale">🔵 Normale</option>
                <option value="Élevée">🟠 Élevée</option>
                <option value="Critique">🔴 Critique</option>
              </select>
              <fas-icon icon="chevron-down" class="text-slate-400 absolute right-3.5 top-1/2 -translate-y-1/2 pointer-events-none text-xs" />
            </div>
          </div>
        </div>
      </div>

      <!-- ===================================================================== -->
      <!-- SECTION 9 — DOCUMENTS DU CHANTIER -->
      <!-- ===================================================================== -->
      <div class="bg-white border border-slate-200 rounded-2xl p-5 sm:p-7 shadow-sm mb-6 space-y-5">
        <div class="flex items-center justify-between pb-3 border-b border-slate-100">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-xl bg-sky-50 text-sky-700 flex items-center justify-center text-lg font-bold">
              <fas-icon icon="file-contract" />
            </div>
            <div>
              <h2 class="text-base sm:text-lg font-bold text-slate-900">9. Documents contractuels & Plans</h2>
              <p class="text-xs text-slate-500">Ajout par Drag & Drop ou sélecteur de fichiers</p>
            </div>
          </div>
          <span class="text-xs font-bold text-slate-500">{{ stagedDocuments.length }} document(s) prêt(s)</span>
        </div>

        <!-- Zone Drag & Drop -->
        <div
          @dragover.prevent="isDragging = true"
          @dragleave.prevent="isDragging = false"
          @drop.prevent="handleFileDrop"
          class="border-2 border-dashed rounded-2xl p-6 text-center transition-all cursor-pointer"
          :class="isDragging ? 'border-blue-500 bg-blue-50/50 scale-[0.99]' : 'border-slate-300 hover:border-blue-400 bg-slate-50/50'"
          @click="$refs.fileInput.click()"
        >
          <input
            ref="fileInput"
            type="file"
            multiple
            class="hidden"
            @change="handleFileInputChange"
          />
          <div class="w-12 h-12 rounded-2xl bg-white border border-slate-200 shadow-sm flex items-center justify-center mx-auto mb-3 text-blue-600 text-xl">
            <fas-icon icon="cloud-arrow-up" />
          </div>
          <p class="text-xs sm:text-sm font-bold text-slate-800">
            Glissez-déposez vos fichiers ici ou <span class="text-blue-600 underline">parcourez votre ordinateur</span>
          </p>
          <p class="text-[11px] text-slate-400 mt-1">
            Formats acceptés : PDF, DWG, DXF, XLSX, DOCX, PNG, JPG (Max 50 Mo par fichier)
          </p>
        </div>

        <!-- Liste des fichiers mis en attente -->
        <div v-if="stagedDocuments.length > 0" class="space-y-2.5">
          <div
            v-for="(doc, idx) in stagedDocuments"
            :key="idx"
            class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 p-3 rounded-xl bg-slate-50 border border-slate-200 text-xs"
          >
            <div class="flex items-center gap-3 min-w-0">
              <div class="w-8 h-8 rounded-lg bg-blue-100 text-blue-700 flex items-center justify-center flex-shrink-0">
                <fas-icon :icon="getFileIcon(doc.file.name)" />
              </div>
              <div class="min-w-0">
                <div class="font-bold text-slate-900 truncate">{{ doc.file.name }}</div>
                <div class="text-[10px] text-slate-400">{{ formatFileSize(doc.file.size) }}</div>
              </div>
            </div>

            <div class="flex items-center gap-2">
              <!-- Choix du type de document -->
              <select
                v-model="doc.document_type"
                class="px-2.5 py-1.5 rounded-lg bg-white border border-slate-200 text-slate-700 text-xs font-medium focus:outline-none focus:border-blue-600"
              >
                <option value="Contrat">Contrat</option>
                <option value="Plan architectural">Plan architectural</option>
                <option value="Devis quantitatif">Devis quantitatif</option>
                <option value="Cahier des charges">Cahier des charges</option>
                <option value="Permis de construire">Permis de construire</option>
                <option value="Autres documents">Autres documents</option>
              </select>

              <!-- Bouton suppression -->
              <button
                type="button"
                @click.stop="removeStagedDocument(idx)"
                class="w-7 h-7 rounded-lg text-slate-400 hover:text-rose-600 hover:bg-rose-50 flex items-center justify-center transition-colors"
                title="Supprimer ce document"
              >
                <fas-icon icon="trash-can" />
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- ===================================================================== -->
      <!-- SECTION 10 — OBSERVATIONS GÉNÉRALES -->
      <!-- ===================================================================== -->
      <div class="bg-white border border-slate-200 rounded-2xl p-5 sm:p-7 shadow-sm mb-6 space-y-3">
        <div class="flex items-center gap-3 pb-2 border-b border-slate-100">
          <div class="w-10 h-10 rounded-xl bg-slate-100 text-slate-600 flex items-center justify-center text-lg font-bold">
            <fas-icon icon="comment-dots" />
          </div>
          <div>
            <h2 class="text-base sm:text-lg font-bold text-slate-900">10. Observations & Remarques générales</h2>
            <p class="text-xs text-slate-500">Notes libres, contraintes environnementales ou instructions spéciales</p>
          </div>
        </div>

        <textarea
          v-model="form.observations"
          rows="3"
          placeholder="Ajoutez ici toutes consignes ou détails utiles pour les équipes terrain et administratives..."
          class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 text-sm focus:outline-none focus:bg-white focus:border-blue-600 transition-all resize-none"
        ></textarea>
      </div>

      <!-- ===================================================================== -->
      <!-- BARRE D'ACTIONS INFERIEURE (STICKY DESKTOP) -->
      <!-- ===================================================================== -->
      <div class="sticky bottom-4 z-20 bg-white/95 backdrop-blur-md border border-slate-200 rounded-2xl p-4 shadow-xl flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div class="flex items-center gap-2 text-xs text-slate-500">
          <fas-icon icon="shield-check" class="text-emerald-600" />
          <span>Formulaire vérifié avec validation FastAPI</span>
        </div>

        <div class="flex items-center gap-2.5 flex-wrap justify-end">
          <!-- Bouton Annuler -->
          <button
            type="button"
            @click="handleCancel"
            class="px-4 py-2.5 rounded-xl border border-slate-200 hover:bg-slate-100 text-slate-700 font-semibold text-xs transition-colors"
            :disabled="submitting"
          >
            Annuler
          </button>

          <!-- Bouton Enregistrer comme brouillon -->
          <button
            type="button"
            @click="handleSubmit(true)"
            class="px-4 py-2.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-800 font-bold text-xs transition-colors flex items-center gap-2"
            :disabled="submitting"
          >
            <fas-icon icon="bookmark" />
            <span>Enregistrer comme brouillon</span>
          </button>

          <!-- Bouton Principal : Créer le chantier -->
          <button
            type="submit"
            class="px-5 py-2.5 rounded-xl bg-[#1d4ed8] hover:bg-blue-800 text-white font-black text-xs sm:text-sm shadow-md transition-all flex items-center gap-2 disabled:opacity-50"
            :disabled="submitting"
          >
            <fas-icon v-if="submitting" icon="spinner" class="animate-spin" />
            <fas-icon v-else icon="check" />
            <span>{{ submitting ? 'Création en cours...' : 'Créer le chantier' }}</span>
          </button>
        </div>
      </div>
    </form>

    <!-- Modale Ajout Type de Chantier -->
    <AddTypeChantierModal
      v-model="showAddTypeModal"
      @created="onTypeCreated"
    />

    <!-- Modale Ajout Responsable -->
    <AddResponsableModal
      v-model="showAddResponsableModal"
      :default-role="modalDefaultRole"
      :target-key="modalTargetKey"
      @created="onResponsableCreated"
    />
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { chantierService } from '@/services'
import { toast, alertSuccess, alertError, confirmDialog } from '@/utils/alert'
import AddTypeChantierModal from './AddTypeChantierModal.vue'
import AddResponsableModal from './AddResponsableModal.vue'

const router = useRouter()

// État du formulaire principal
const form = reactive({
  code: '',
  name: '',
  description: '',
  type_id: null,
  type_name: '',
  status: 'En préparation',

  // Localisation
  country: "Côte d'Ivoire",
  city: 'Abidjan',
  commune: '',
  district: '',
  address: '',
  latitude: null,
  longitude: null,

  // Client
  client_id: null,
  client_name: '',

  // Responsables
  project_manager_id: null,
  site_manager_id: null,
  foreman_id: null,
  hse_officer_id: null,
  design_office: '',
  contractor: '',

  // Planning
  start_date_planned: '',
  end_date_planned: '',
  estimated_duration_days: 0,
  start_date_actual: '',
  end_date_actual: '',

  // Finances
  budget_estimated: null,
  cost_estimated: null,
  contract_amount: null,
  currency: 'FCFA',
  funding_mode: 'Fonds propres',

  // Technique
  surface_m2: null,
  buildings_count: null,
  floors_count: null,
  soil_nature: '',
  construction_method: '',
  technical_description: '',

  // Suivi initial
  physical_progress: 0,
  financial_progress: 0,
  priority: 'Normale',

  observations: '',
  is_draft: false,
})

// Mode client : 'existing' ou 'new'
const clientMode = ref('existing')
const newClient = reactive({
  type: 'Particulier',
  name: '',
  phone: '',
  email: '',
  address: '',
  contact_person: '',
  company_name: '',
  rccm: '',
  company_contact: '',
  ministry: '',
  direction: '',
  service: '',
  admin_in_charge: '',
})

// Erreurs de validation champ par champ
const errors = reactive({
  name: '',
  type_id: '',
  city: '',
  client_id: '',
  client_name: '',
  start_date_planned: '',
  end_date_planned: '',
})

// Données référentielles
const chantierTypes = ref([])
const responsablesList = ref([])
const clientsList = ref([])

// Documents prêts au dépôt
const stagedDocuments = ref([])
const isDragging = ref(false)

// Modales & Chargements
const showAddTypeModal = ref(false)
const showAddResponsableModal = ref(false)
const modalDefaultRole = ref('Conducteur des travaux')
const modalTargetKey = ref('site_manager_id')

const loadingCode = ref(false)
const locatingGps = ref(false)
const submitting = ref(false)

// -----------------------------------------------------------------------------
// Calculs réactifs (Durée estimée, Formatage devise, etc.)
// -----------------------------------------------------------------------------
const calculatedDurationDays = computed(() => {
  if (!form.start_date_planned || !form.end_date_planned) return 0
  const d1 = new Date(form.start_date_planned)
  const d2 = new Date(form.end_date_planned)
  if (isNaN(d1) || isNaN(d2) || d2 < d1) return 0
  const diffTime = Math.abs(d2 - d1)
  return Math.ceil(diffTime / (1000 * 60 * 60 * 24))
})

const calculatedDurationText = computed(() => {
  const days = calculatedDurationDays.value
  if (days <= 0) return '—'
  if (days < 30) return `${days} jours`
  const months = (days / 30).toFixed(1)
  return `${days} jours (~ ${months} mois)`
})

watch(calculatedDurationDays, (val) => {
  form.estimated_duration_days = val
})

const selectedClientSummary = computed(() => {
  if (!form.client_id) return null
  return clientsList.value.find((c) => c.id === form.client_id) || null
})

function filteredResponsables(role) {
  // Affiche d'abord ceux qui correspondent au rôle, puis tous les autres
  return [
    ...responsablesList.value.filter((r) => r.role_name === role),
    ...responsablesList.value.filter((r) => r.role_name !== role),
  ]
}

function formatCurrencyDisplay(val) {
  if (!val || isNaN(val)) return `0 ${form.currency}`
  return `${new Intl.NumberFormat('fr-FR').format(val)} ${form.currency}`
}

function formatFileSize(bytes) {
  if (!bytes) return '0 o'
  if (bytes < 1024) return `${bytes} o`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} Ko`
  return `${(bytes / (1024 * 1024)).toFixed(1)} Mo`
}

function getFileIcon(filename) {
  const ext = filename.split('.').pop()?.toLowerCase()
  if (ext === 'pdf') return 'file-pdf'
  if (['xls', 'xlsx', 'csv'].includes(ext)) return 'file-excel'
  if (['doc', 'docx'].includes(ext)) return 'file-word'
  if (['png', 'jpg', 'jpeg'].includes(ext)) return 'file-image'
  return 'file-lines'
}

// -----------------------------------------------------------------------------
// Chargement initial des données depuis FastAPI
// -----------------------------------------------------------------------------
async function fetchNextCode() {
  loadingCode.value = true
  try {
    const data = await chantierService.getNextCode()
    form.code = data.next_code
  } catch (err) {
    console.error('Erreur génération code:', err)
  } finally {
    loadingCode.value = false
  }
}

async function loadReferentials() {
  try {
    const [types, resps, clients] = await Promise.all([
      chantierService.getTypes(),
      chantierService.getResponsables(),
      chantierService.getClients(),
    ])
    chantierTypes.value = types
    responsablesList.value = resps
    clientsList.value = clients

    // Sélection par défaut du premier type s'il existe
    if (!form.type_id && types.length > 0) {
      form.type_id = types[0].id
      form.type_name = types[0].name
    }
  } catch (err) {
    console.error('Erreur chargement référentiels:', err)
  }
}

onMounted(() => {
  fetchNextCode()
  loadReferentials()

  // Dates par défaut réalistes (+3 mois)
  const today = new Date()
  const inThreeMonths = new Date()
  inThreeMonths.setMonth(today.getMonth() + 3)

  form.start_date_planned = today.toISOString().split('T')[0]
  form.end_date_planned = inThreeMonths.toISOString().split('T')[0]
})

// -----------------------------------------------------------------------------
// Événements modales inline [+] & Sélections dynamiques
// -----------------------------------------------------------------------------
function handleTypeChange() {
  const t = chantierTypes.value.find((item) => item.id === form.type_id)
  if (t) form.type_name = t.name
}

function onTypeCreated(newType) {
  chantierTypes.value.push(newType)
  form.type_id = newType.id
  form.type_name = newType.name
}

function openAddResponsableModal(role, targetKey) {
  modalDefaultRole.value = role
  modalTargetKey.value = targetKey
  showAddResponsableModal.value = true
}

function onResponsableCreated({ responsable, targetKey }) {
  responsablesList.value.push(responsable)
  if (targetKey && form[targetKey] !== undefined) {
    form[targetKey] = responsable.id
  }
}

function handleClientSelect() {
  const c = clientsList.value.find((item) => item.id === form.client_id)
  if (c) form.client_name = c.name
}

// -----------------------------------------------------------------------------
// Géolocalisation GPS
// -----------------------------------------------------------------------------
function locateGps() {
  if (!navigator.geolocation) {
    toast('La géolocalisation n’est pas supportée par votre navigateur.', 'warning')
    return
  }
  locatingGps.value = true
  navigator.geolocation.getCurrentPosition(
    (position) => {
      form.latitude = parseFloat(position.coords.latitude.toFixed(6))
      form.longitude = parseFloat(position.coords.longitude.toFixed(6))
      locatingGps.value = false
      toast(`Position GPS capturée : [${form.latitude}, ${form.longitude}]`, 'success')
    },
    (err) => {
      locatingGps.value = false
      toast(`Impossible de récupérer la position : ${err.message}`, 'warning')
    },
    { enableHighAccuracy: true, timeout: 8000 }
  )
}

// -----------------------------------------------------------------------------
// Gestion des Fichiers & Drag / Drop
// -----------------------------------------------------------------------------
function handleFileDrop(e) {
  isDragging.value = false
  const files = Array.from(e.dataTransfer?.files || [])
  addFiles(files)
}

function handleFileInputChange(e) {
  const files = Array.from(e.target?.files || [])
  addFiles(files)
  e.target.value = ''
}

function addFiles(files) {
  files.forEach((file) => {
    stagedDocuments.value.push({
      file,
      document_type: 'Contrat',
    })
  })
  toast(`${files.length} document(s) ajouté(s) à la liste`, 'info')
}

function removeStagedDocument(index) {
  stagedDocuments.value.splice(index, 1)
}

// -----------------------------------------------------------------------------
// Validation & Soumission
// -----------------------------------------------------------------------------
function validate() {
  let isValid = true
  Object.keys(errors).forEach((k) => (errors[k] = ''))

  if (!form.name.trim()) {
    errors.name = 'Le nom du chantier est obligatoire.'
    isValid = false
  }

  if (!form.type_id) {
    errors.type_id = 'Le type de chantier est obligatoire.'
    isValid = false
  }

  if (!form.city.trim()) {
    errors.city = 'La ville est obligatoire.'
    isValid = false
  }

  if (clientMode.value === 'existing') {
    if (!form.client_id) {
      errors.client_id = 'Veuillez sélectionner un client dans la liste.'
      isValid = false
    }
  } else {
    if (!newClient.name.trim()) {
      errors.client_name = 'Le nom ou raison sociale du client est obligatoire.'
      isValid = false
    }
  }

  if (!form.start_date_planned) {
    errors.start_date_planned = 'La date de début prévue est obligatoire.'
    isValid = false
  }

  if (!form.end_date_planned) {
    errors.end_date_planned = 'La date de fin prévue est obligatoire.'
    isValid = false
  } else if (form.start_date_planned && form.end_date_planned < form.start_date_planned) {
    errors.end_date_planned = 'La date de fin ne peut pas être antérieure à la date de début.'
    isValid = false
  }

  return isValid
}

async function handleSubmit(asDraft = false) {
  if (!asDraft && !validate()) {
    toast('Veuillez renseigner tous les champs obligatoires.', 'warning')
    return
  }

  submitting.value = true
  form.is_draft = asDraft

  try {
    const payload = {
      ...form,
      start_date_actual: form.start_date_actual || null,
      end_date_actual: form.end_date_actual || null,
    }

    if (clientMode.value === 'new') {
      payload.client_id = null
      payload.new_client = { ...newClient }
    }

    // 1. Création du chantier dans FastAPI
    const createdChantier = await chantierService.createChantier(payload)

    // 2. Téléversement des documents en attente s'il y en a
    if (stagedDocuments.value.length > 0) {
      for (const item of stagedDocuments.value) {
        try {
          await chantierService.uploadDocument(
            createdChantier.id,
            item.document_type,
            item.file
          )
        } catch (fileErr) {
          console.error(`Erreur upload ${item.file.name}:`, fileErr)
        }
      }
    }

    // 3. Notification de succès
    const title = asDraft ? 'Brouillon enregistré' : 'Chantier créé avec succès !'
    const message = `Le chantier <strong>${createdChantier.name}</strong> (Réf: <strong>${createdChantier.code}</strong>) a été enregistré.`

    await alertSuccess(title, message)

    // 4. Redirection vers la page de détail du chantier
    router.push(`/chantiers/${createdChantier.id}`)
  } catch (err) {
    console.error('Erreur lors de la création du chantier:', err)
    const detail = err.response?.data?.detail
    const msg = typeof detail === 'string' ? detail : 'Une erreur est survenue lors de la création du chantier.'
    alertError('Erreur de création', msg)
  } finally {
    submitting.value = false
  }
}

async function handleCancel() {
  const ok = await confirmDialog(
    'Annuler la création ?',
    'Toutes les données saisies non sauvegardées seront perdues.',
    'Oui, quitter'
  )
  if (ok) {
    router.push('/chantiers')
  }
}
</script>
